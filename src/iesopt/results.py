import warnings
import pandas as pd

from .util import get_iesopt_module_attr


class ddict(dict):
    """Wrapper to enable dot.notation access to dictionary attributes."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Results:
    _valid_attrs = ["attributes", "model", "custom", "input", "info", "snapshots", "components"]

    def __init__(self, file: str = None, model=None):
        """
        Create a new `Results` object, either from a file or from an IESopt model. Make sure to pass either a file or a
        model explicitly using a keyword argument.

        :param file: Path to the results file to load, by default None
        :param model: IESopt model to extract results from, by default None

        :type file: str, optional
        :type model: IESopt.Model, optional
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

    def entries(self, field: str = None):
        """
        Get all available entries for a specific field, or all fields if `field` is `None`.

        Parameters
        ----------
        field : str, optional
            Field to get entries for, by default None which returns all fields
        """
        if field is None:
            return [it for it in Results._valid_attrs if getattr(self, f"_{it}") is not None]
        return sorted(getattr(self, field).keys())

    def to_dict(self, filter=None, field_types=None, build_cache: bool = True):
        """
        Extract results from the `Results` object and return them as a dictionary.

        Parameters
        ----------
        filter : callable, optional
            Filter function to apply to the results, by default None, must take three arguments: (c, t, f) where `c` is
            the component's name, `t` is the field type ("var", "exp", "con", or "obj"), and `f` is the field name
        field_types : list[str], optional
            Field types to extract, by default None, which extracts all field types
        build_cache : bool, optional
            Whether to build a cache of the results, by default True
        """
        if build_cache:
            self._build_cache()

        if field_types is None:
            field_types = ["var", "exp", "con", "obj"]

        entries = {}
        if self._cache is None:
            for c in self.model["components"].keys():
                for t in field_types:
                    container = getattr(self.model["components"][c], t)
                    for f in [str(it) for it in self._julia.Main.keys(container)]:
                        if (filter is None) or filter(c, t, f):
                            entries[(c, t, f)] = Results._safe_convert(getattr(container, f))
        else:
            for c, t, f in self._cache.keys():
                if (t in field_types) and ((filter is None) or filter(c, t, f)):
                    entries[(c, t, f)] = self._cache[(c, t, f)]

        return entries

    def to_pandas(self, filter=None, field_types=None, orientation: str = "long", build_cache: bool = True):
        """
        Extract results from the `Results` object and return them as `pd.DataFrame` or `pd.Series` (depending on the
        shape of the included results).

        Parameters
        ----------
        filter : callable, optional
            Filter function to apply to the results, by default None, must take three arguments: (c, t, f) where `c` is
            the component's name, `t` is the field type ("var", "exp", "con", or "obj"), and `f` is the field name
        field_types : list[str], optional
            Field types to extract, by default None, which extracts all field types
        orientation : str, optional
            Orientation of the resulting DataFrame, either "wide" or "long", by default "long"
        build_cache : bool, optional
            Whether to build a cache of the results, by default True
        """
        _dict = self.to_dict(filter, field_types, build_cache)

        if orientation == "wide":
            _result_types = set(type(it) for it in _dict.values())

            if len(_result_types) == 1:
                if _result_types.pop() in [int, float]:
                    return pd.Series(_dict)

                return pd.DataFrame(_dict)

            warnings.warn(
                "Results must be of the same shape (= length) to create a DataFrame, with `orientation='wide'`. "
                "Falling back to `orientation='long'`. This warning can be prevented by calling `results.to_pandas("
                "orientation='long') instead, or by applying filters (using `filter` and/or `field_types`) that only "
                "select results of the same shape (example: objectives are always scalars, while most variables - "
                "except Decisions - are vector valued, indexed over all snapshots)."
            )
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

            return pd.DataFrame(_data)

        raise ValueError(f"`orientation` can be 'wide' or 'long', got '{orientation}'.")

    def __getattr__(self, attr: str):
        if attr not in Results._valid_attrs:
            raise Exception(f"Attribute '{attr}' is not accessible, pick one of {Results._valid_attrs}")
        if not hasattr(self, f"_{attr}"):
            raise Exception(f"`Results` object has no attribute '{attr}'")
        if getattr(self, f"_{attr}") is None:
            raise Exception(f"Attribute '{attr}' not properly loaded, consider checking `results.entries()` first")
        return getattr(self, f"_{attr}")

    def _build_cache(self):
        if self._cache is None:
            self._cache = self.to_dict(build_cache=False)

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
            "components": model.data.results.components,
            "objectives": model.data.results.objectives,
            "custom": model.data.results.customs,
        }
        self._snapshots = [model.data.model.snapshots[t].name for t in model.data.model.T]
        self._components = sorted(model.data.results.components.keys())

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
        # if isinstance(value, self._julia.VectorValue):
        #     return self._julia.PythonCall.pylist(value)
        # if isinstance(value, self._julia.DictValue):
        #     return {str(k): cls._safe_convert(v) for (k, v) in value.items()}
        return value
