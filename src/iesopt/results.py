import warnings
import re
import pandas as pd
import numpy as np
from pydantic import validate_call

from .util import get_iesopt_module_attr
from .julia import jl_isa


class ddict(dict):
    """Wrapper to enable dot.notation access to dictionary attributes."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class JuliaCallPyConvertReadWrapper:
    def __init__(self, obj):
        import juliacall

        self._juliacall = juliacall
        self._obj = obj

    def keys(self):
        if isinstance(self._obj, dict | self._juliacall.DictValue):
            return dict(self._obj).keys()
        raise TypeError(f"Object of type '{type(self._obj)}' inside JuliaCallPyConvertReadWrapper has no keys")

    def __len__(self):
        if isinstance(self._obj, dict | list | tuple | self._juliacall.DictValue | self._juliacall.VectorValue):
            return len(self._obj)
        raise TypeError(f"Object of type '{type(self._obj)}' inside JuliaCallPyConvertReadWrapper has no length")

    def _rewrap_return(self, value):
        if isinstance(value, self._juliacall.ArrayValue):
            return value.to_numpy(copy=False)
        if isinstance(value, float | int | str | bool | type(None)):
            return value

        if isinstance(value, self._juliacall.DictValue):
            return JuliaCallPyConvertReadWrapper(value)

        # Some other/unknown type, rewrap it.
        return JuliaCallPyConvertReadWrapper(value)

    def __getattr__(self, name: str):
        return self._rewrap_return(getattr(self._obj, name))

    def __getitem__(self, key):
        return self._rewrap_return(self._obj.get(key))


class Results:
    _valid_attrs = ["attributes", "model", "custom", "input", "info", "snapshots", "components"]

    @validate_call
    def __init__(self, *, file: str = None, model=None):
        """
        Create a new `Results` object, either from a file or from an IESopt model. Make sure to pass either a file or a
        model explicitly using a keyword argument.

        Keyword Arguments
            file : Optional[str]
                Path to the results file to load, by default None
            model : Optional[IESopt.Model]
                IESopt model to extract results from, by default None
        """
        self._attributes = None
        self._model = None
        self._snapshots = None
        self._components = None
        self._custom = None
        self._input = None
        self._info = None
        self._source = None

        self._cache = None

        self._IESopt = get_iesopt_module_attr("IESopt")
        self._julia = get_iesopt_module_attr("julia")

        if (int(file is None) + int(model is None)) != 1:
            raise Exception("Either file or model must be set, not both and not none of them.")
        elif file is not None:
            if not isinstance(file, str):
                raise Exception("File must be a `str`, did you try passing a model without `model=your_model`?")
            self._from_file(file)
        elif model is not None:
            self._from_model(model)

        # Allow dot access to attributes of "model" results, to align with access to the models structure.
        self._model = ddict(self._model)

    @property
    def components(self):
        return JuliaCallPyConvertReadWrapper(self._model["components"])

    @property
    def objectives(self):
        return JuliaCallPyConvertReadWrapper(self._model["objectives"])

    @property
    def customs(self):
        return JuliaCallPyConvertReadWrapper(self._model["customs"])

    @validate_call
    def get(
        self,
        result: str,
        component: str,
        fieldtype: str,
        field: str,
        *,
        mode: str = "primal",
        build_cache: bool = False,
    ):
        if result not in ["component", "objective", "custom"]:
            raise ValueError(f"`result` must be 'component', 'objective', or 'custom', got '{result}'")

        if result in ["objective", "custom"]:
            # TODO: Implement and remove this
            raise NotImplementedError("Accessing objectives and custom results is not yet supported using `get(...)`")

        if mode == "dual":
            field = field + "__dual"
        elif mode != "primal":
            raise ValueError(f"`mode` must be 'primal' or 'dual', got '{mode}'")

        if build_cache:
            self._build_cache()

        if self._has_cache():
            t = (component, fieldtype, field)
            if t in self._cache:
                return self._cache[t]
            raise ValueError(f"Failed to access result '{fieldtype}.{field}' in component '{component}'")

        return self._get_safe(component, fieldtype, field, mode)

    @validate_call
    def query_available_results(self, component: str, mode: str = "both"):
        """
        Query the available results for a specific component, optionally filtered by `mode`.

        Arguments:
            component : str
                Component to query results for
            mode : Optional[str]
                Mode to query results for, either "both", "primal", or "dual", by default "both"
        """
        regex = re.compile(component)

        if not self._has_cache():
            self._build_cache()

        if mode == "both":
            return [
                (it[1], (x := it[2].split("__"))[0], "primal" if len(x) == 1 else "dual")
                for it in self._cache
                if re.search(regex, it[0])
            ]
        elif mode == "primal":
            return [(it[1], it[2]) for it in self._cache if re.search(regex, it[0]) and "__dual" not in it[2]]
        elif mode == "dual":
            return [
                (it[1], it[2].split("__")[0]) for it in self._cache if re.search(regex, it[0]) and "__dual" in it[2]
            ]
        else:
            raise ValueError("Invalid mode, must be either 'both', 'primal', or 'dual'")

    @validate_call
    def entries(self, field: str = None):
        """
        Get all available entries for a specific field, or all fields if `field` is `None`.

        Arguments:
            field : Optional[str]
                Field to get entries for, by default None which returns all fields
        """
        if field is None:
            return [it for it in Results._valid_attrs if getattr(self, f"_{it}") is not None]
        return sorted(getattr(self, field).keys())

    @validate_call
    def to_dict(self, filter=None, field_types=None, build_cache: bool = True) -> dict:
        """
        Extract results from the `Results` object and return them as a dictionary.

        Arguments:
            filter : Optional[Callable]
                Filter function to apply to the results, by default None, must take three arguments: (c, t, f) where `c` is
                the component's name, `t` is the field type ("var", "exp", "con", or "obj"), and `f` is the field name.
            field_types : Optional[list[str]]
                Field types to extract, by default None, which extracts all field types.
            build_cache : Optional[bool]
                Whether to build a cache of the results, by default True.

        Returns:
            Dictionary of results, with keys as tuples of (component, fieldtype, field) and values as the result.
        """
        if build_cache:
            self._build_cache()

        if field_types is None:
            field_types = ["var", "exp", "con", "obj", "res"]

        entries = {}
        if self._cache is None:
            for c in self._model["components"].keys():
                for t in field_types:
                    container = getattr(self._model["components"][c], t)
                    for f in [str(it) for it in self._julia.Main.keys(container)]:
                        if (filter is None) or filter(c, t, f):
                            entries[(c, t, f)] = Results._safe_convert(getattr(container, f))
        else:
            for c, t, f in self._cache.keys():
                if (t in field_types) and ((filter is None) or filter(c, t, f)):
                    entries[(c, t, f)] = self._cache[(c, t, f)]

        return entries

    @validate_call
    def to_pandas(self, filter=None, field_types=None, orientation: str = "long", build_cache: bool = True):
        """
        Extract results from the `Results` object and return them as :py:class:`pandas.DataFrame` or :py:class:`pandas.Series` (depending on the
        shape of the included results).

        Arguments:
            filter : Optional[Callable]
                Filter function to apply to the results, by default None, must take three arguments: (c, t, f) where `c` is
                the component's name, `t` is the field type ("var", "exp", "con", or "obj"), and `f` is the field name
            field_types : Optional[list[str]]
                Field types to extract, by default None, which extracts all field types
            orientation : Optional[str]
                Orientation of the resulting DataFrame, either "wide" or "long", by default "long"
            build_cache : Optional[bool]
                Whether to build a cache of the results, by default True.

        Returns:
            DataFrame or Series of results, depending on the orientation and shape of the results.
        """
        _dict = self.to_dict(filter, field_types, build_cache)

        # Check if we can cast to `pd.Series` (no matter the orientation).
        _result_types = set(type(it) for it in _dict.values())
        if len(_result_types) == 1:
            _rt = _result_types.pop()
            if _rt in [int, float]:
                return pd.Series(_dict)

            if _rt == np.ndarray:
                if len(_dict) == 1:
                    k, v = next(iter(_dict.items()))

                    if isinstance(v, int | float):
                        return pd.Series(v, index=k)

                    value_shape = v.shape
                    if len(value_shape) == 1:
                        if value_shape[0] == len(self._snapshots):
                            return pd.Series(v, index=self._snapshots, name=k)

            if orientation == "wide":
                return pd.DataFrame(_dict, index=self._snapshots)

        if orientation == "wide":
            warnings.warn(
                "Results must be of the same shape (= length) to create a DataFrame, with `orientation='wide'`. "
                "Falling back to `orientation='long'`. This warning can be prevented by calling `results.to_pandas("
                "orientation='long') instead, or by applying filters (using `filter` and/or `field_types`) that only "
                "select results of the same shape (example: objectives are always scalars, while most variables - "
                "except Decisions - are vector valued, indexed over all snapshots)."
            )
            warnings.warn(f"Got the following result types: {_result_types}")
            orientation = "long"

        if orientation == "long":
            n_snapshots = len(self._snapshots)
            _data = {c: [] for c in ["snapshot", "component", "fieldtype", "field", "value", "mode"]}

            for (c, t, f), v in _dict.items():
                m = "primal"
                if f.endswith("__dual"):
                    f = f[:-6]
                    m = "dual"

                if isinstance(v, (int, float)):
                    _data["snapshot"].append(None)
                    _data["component"].append(c)
                    _data["fieldtype"].append(t)
                    _data["field"].append(f)
                    _data["value"].append(v)
                    _data["mode"].append(m)
                else:
                    _data["snapshot"].extend(self._snapshots)
                    _data["component"].extend([c] * n_snapshots)
                    _data["fieldtype"].extend([t] * n_snapshots)
                    _data["field"].extend([f] * n_snapshots)
                    _data["value"].extend(v)
                    _data["mode"].extend([m] * n_snapshots)

            try:
                return pd.DataFrame(_data)
            except Exception:
                warnings.warn(
                    "Failed to create DataFrame. This is mostlikely due to non aligned result shapes. A "
                    "common cause are custom results, registered inside an addon, that have a different "
                    "temporal resolution than the main model results. Consider filtering out such results."
                )
                return None

        raise ValueError(f"`orientation` can be 'wide' or 'long', got '{orientation}'.")

    @validate_call
    def overview(self, component: str, *, temporal: bool, mode: str = "both"):
        regex = re.compile(component)

        if not self._has_cache():
            self._build_cache()

        if mode == "both":
            ret = {
                (k[0], k[1], (x := k[2].split("__"))[0], "primal" if len(x) == 1 else "dual"): v
                for (k, v) in self._cache.items()
                if re.search(regex, k[0]) and isinstance(v, int | float) != temporal
            }
        elif mode == "primal":
            ret = {
                (k[0], k[1], k[2], "primal"): v
                for (k, v) in self._cache.items()
                if re.search(regex, k[0]) and "__dual" not in k[2] and isinstance(v, int | float) != temporal
            }
        elif mode == "dual":
            ret = {
                (k[0], k[1], k[2].split("__")[0], "dual"): v
                for (k, v) in self._cache.items()
                if re.search(regex, k[0]) and "__dual" in k[2] and isinstance(v, int | float) != temporal
            }
        else:
            raise ValueError("Invalid mode, must be either 'both', 'primal', or 'dual'")

        if len(ret) == 0:
            return None

        if temporal:
            return pd.DataFrame(ret, index=self._snapshots).sort_index(axis=1)
        else:
            return pd.Series(ret)

    # def __getattr__(self, attr: str):
    #     if attr not in Results._valid_attrs:
    #         raise Exception(f"Attribute '{attr}' is not accessible, pick one of {Results._valid_attrs}")
    #     if not hasattr(self, f"_{attr}"):
    #         raise Exception(f"`Results` object has no attribute '{attr}'")
    #     if getattr(self, f"_{attr}") is None:
    #         raise Exception(f"Attribute '{attr}' not properly loaded, consider checking `results.entries()` first")
    #     return getattr(self, f"_{attr}")

    def _build_cache(self):
        if self._cache is None:
            self._cache = self.to_dict(build_cache=False)

    def _has_cache(self):
        return self._cache is not None

    def _get_safe(self, component: str, fieldtype: str, field: str, mode: str = "primal"):
        if mode not in ["primal", "dual"]:
            raise ValueError(f"`mode` must be 'primal' or 'dual', got '{mode}'.")

        try:
            components = self._model["components"]
        except Exception:
            raise ValueError("Failed to access `components` in model results")
        try:
            all_results = components[component]
        except Exception:
            raise ValueError(f"Failed to access component '{component}' in model results")
        try:
            container = getattr(all_results, fieldtype)
        except Exception:
            raise ValueError(f"Failed to access results for `fieldtype` '{fieldtype}' in component '{component}'")
        try:
            result = getattr(container, field)
        except Exception:
            raise ValueError(f"Failed to access result '{field}' in component '{component}'")

        return Results._safe_convert(result)

    def _from_file(self, file: str):
        results = self._IESopt.load_results(file)

        result_entries = ddict({})
        for key in results.keys():
            _current = result_entries
            _keys = key.split("/")
            for i in range(len(_keys)):
                if i == len(_keys) - 1:
                    _current[_keys[i]] = Results._safe_convert(results[key])
                else:
                    _current[_keys[i]] = _current.get(_keys[i], ddict({}))
                    _current = _current[_keys[i]]

        for key in result_entries.keys():
            if hasattr(self, f"_{key}"):
                if getattr(self, f"_{key}") is None:
                    setattr(self, f"_{key}", result_entries[key])
                else:
                    raise Exception(f"Duplicate result entry: {key}")
            else:
                raise Exception(f"Unknown result entry: {key}")

        snapshots = results["model/snapshots"]
        self._snapshots = [snapshots[t].name for t in sorted(snapshots.keys())]
        self._components = sorted(results["model/components"].keys())
        self._source = file

    def _from_model(self, model):
        self._source = "an IESopt model"
        self._model = {
            "components": model.internal.results.components,
            "objectives": model.internal.results.objectives,
            "custom": model.internal.results.customs,
        }
        self._snapshots = [model.internal.model.snapshots[t].name for t in model.internal.model.T]
        self._components = sorted(model.internal.results.components.keys())

    def __repr__(self) -> str:
        _sep = "', '"
        return (
            "An IESopt result object:"
            + f"\n\tsource: {self._source}"
            + "\n\tattributes: "
            + (
                f"'{self.entries('attributes')[0]}', ..., '{self.entries('attributes')[-1]}'"
                if self._attributes is not None
                else "none"
            )
            + f"\n\tmodel results: {'yes' if self._model is not None else 'no'}"
            + "\n\tcustom results: "
            + (f"{len(self._custom)}" if self._custom is not None and len(self._custom) > 0 else "no")
            + "\n\tinput fields: "
            + (f"'{_sep.join(self._input)}'" if self._input is not None else "none")
            + "\n\tinfo fields: "
            + (f"'{_sep.join(self._info)}'" if self._info is not None else "none")
        )

    @classmethod
    def _safe_convert(cls, value):
        # TODO: ensure recursive conversion of all multi-element types
        if jl_isa(value, "AbstractVector"):
            return value.to_numpy(copy=False)
        if jl_isa(value, "AbstractDict"):
            return dict(value)
        if jl_isa(value, "AbstractSet"):
            return set(value)
        return value
