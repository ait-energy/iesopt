from enum import Enum
from pathlib import Path
from warnings import warn

from .util import logger, get_iesopt_module_attr
from .julia.util import jl_symbol, recursive_convert_py2jl
from .results import Results


class ModelStatus(Enum):
    """Status of an :py:class:`iesopt.Model`."""

    EMPTY = "empty"
    GENERATED = "generated"
    FAILED_GENERATE = "failed_generate"
    FAILED_OPTIMIZE = "failed_optimize"
    OPTIMAL = "optimal"
    OPTIMAL_LOCALLY = "local_optimum"
    INFEASIBLE = "infeasible"
    INFEASIBLE_OR_UNBOUNDED = "infeasible_unbounded"
    OTHER = "other"


class Model:
    """An IESopt model, based on an :jl:module:`IESopt.jl <IESopt.IESopt>` core model."""

    def __init__(self, filename: str | Path, **kwargs) -> None:
        self._filename = filename
        self._kwargs = recursive_convert_py2jl(kwargs)

        self._model = None
        self._verbosity = kwargs.get("verbosity", True)

        self._status = ModelStatus.EMPTY
        self._status_details = None

        self._results = None

        self._IESopt = get_iesopt_module_attr("IESopt")
        self._JuMP = get_iesopt_module_attr("JuMP")
        self._jump_value = get_iesopt_module_attr("jump_value")
        self._jump_dual = get_iesopt_module_attr("jump_dual")

    def __repr__(self) -> str:
        if self._model is None:
            return "An IESopt model (not yet generated)"

        n_var = self._JuMP.num_variables(self.core)
        n_con = self._JuMP.num_constraints(self.core, count_variable_in_set_constraints=False)
        solver = self._JuMP.solver_name(self.core)
        termination_status = self._JuMP.termination_status(self.core)

        return (
            f"An IESopt model:"
            f"\n\tname: {self.data.input.config['general']['name']['model']}"
            f"\n\tsolver: {solver}"
            f"\n\t"
            f"\n\t{n_var} variables, {n_con} constraints"
            f"\n\tstatus: {termination_status}"
        )

    @property
    def core(self):
        """Access the core `JuMP` model that is used internally."""
        if self._model is None:
            raise Exception("Model was not properly set up; call `generate` first")
        return self._model

    @property
    def data(self):
        """Access the IESopt data object of the model.

        This is deprecated; use `model.internal` instead (similar to the Julia usage `IESopt.internal(model)`).
        """
        warn(
            "Using `model.data` is deprecated; use `model.internal` instead (similar to the Julia usage `IESopt.internal(model)`)",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.internal

    @property
    def internal(self):
        """Access the IESopt data object of the model."""
        return self._IESopt.internal(self.core)

    @property
    def status(self) -> ModelStatus:
        """Get the current status of this model. See `ModelStatus` for possible values."""
        return self._status

    @property
    def objective_value(self) -> float:
        """Get the objective value of the model. Only available if the model was solved beforehand."""
        if self._status == ModelStatus.OPTIMAL_LOCALLY:
            logger.warning("Model is only locally optimal; objective value may not be accurate")
        elif self._status != ModelStatus.OPTIMAL:
            raise Exception("Model is not optimal; no objective value available")
        return self._JuMP.objective_value(self.core)

    def generate(self) -> None:
        """Generate a IESopt model from the attached top-level YAML config."""
        try:
            self._model = self._IESopt.generate_b(str(self._filename), **self._kwargs)
            self._status = ModelStatus.GENERATED
        except Exception as e:
            self._status = ModelStatus.FAILED_GENERATE
            logger.error(f"Exception during `generate`: {e}")
            try:
                logger.error(f"Current debugging info: {self.data.debug}")
            except Exception as e:
                logger.error("Failed to extract debugging info")

    def optimize(self) -> None:
        """Optimize the model."""
        try:
            self._IESopt.optimize_b(self.core)

            if self._JuMP.is_solved_and_feasible(self.core, allow_local=False):
                self._status = ModelStatus.OPTIMAL
                self._results = Results(model=self)
            elif self._JuMP.is_solved_and_feasible(self.core, allow_local=True):
                self._status = ModelStatus.OPTIMAL_LOCALLY
                self._results = Results(model=self)
            else:
                _term_status = self._JuMP.termination_status(self.core)
                if str(_term_status) == "INFEASIBLE":
                    self._status = ModelStatus.INFEASIBLE
                elif str(_term_status) == "INFEASIBLE_OR_UNBOUNDED":
                    self._status = ModelStatus.INFEASIBLE_OR_UNBOUNDED
                else:
                    self._status = ModelStatus.OTHER
                    self._status_details = _term_status
        except Exception as e:
            self._status = ModelStatus.FAILED_OPTIMIZE
            logger.error(f"Exception during `optimize`: {e}")
            try:
                logger.error(f"Current debugging info: {self.data.debug}")
            except Exception as e:
                logger.error("Failed to extract debugging info")

    @property
    def results(self) -> Results:
        """Get the results of the model."""
        if self._results is None:
            raise Exception("No results available; have you successfully called `optimize`?")
        return self._results

    def extract_result(self, component: str, field: str, mode: str = "value"):
        """Manually extract a specific result from the model."""
        try:
            c = self._IESopt.get_component(self.core, component)
        except Exception:
            raise Exception(f"Exception during `extract_result({component}, {field}, mode={mode})`")

        f = None
        for fieldtype in ["var", "exp", "con", "obj"]:
            try:
                t = getattr(c, fieldtype)
                f = getattr(t, field)
                break
            except Exception:
                pass

        if f is None:
            raise Exception(f"Field `{field}` not found in component `{component}`")

        try:
            if mode == "value":
                return self._jump_values(f)
            elif mode == "dual":
                return self._jump_duals(f)
            else:
                raise Exception(f"Mode `{mode}` not supported, use `value` or `dual`")
        except Exception:
            raise Exception(f"Error during extraction of result `{field}` from component `{component}`")

    def get_component(self, component: str):
        """Get a core component based on its full name."""
        try:
            return self._IESopt.get_component(self.core, component)
        except Exception:
            raise Exception(f"Error while retrieving component `{component}` from model")

    def get_components(self, tagged=None):
        """
        Get all components of the model, possibly filtered by (a) tag(s).

        Arguments:
            tagged (str or list of str): The tag(s) to filter the components by, can be `None` (default) to get all components.
        """
        if tagged is None:
            return self._IESopt.get_components(self.core)

        return self._IESopt.get_components(self.core, recursive_convert_py2jl(tagged))

    def get_variable(self, component: str, variable: str):
        """Get a specific variable from a core component."""
        raise DeprecationWarning(
            f"`get_variable(...)` is deprecated; you can instead access the variable directly using "
            f"`model.get_component('{component}').var.{variable}`. Conversion to Python lists, if not done "
            f"automatically, can be done using `list(...)`."
        )

    def get_constraint(self, component: str, constraint: str):
        """Get a specific constraint from a core component."""
        raise DeprecationWarning(
            f"`get_constraint(...)` is deprecated; you can instead access the constraint directly using "
            f"`model.get_component('{component}').con.{constraint}`. Conversion to Python lists, if not done "
            f"automatically, can be done using `list(...)`."
        )

    def nvar(self, var: str):
        """Extract a named variable, from `model`.

        If your variable is called `:myvar`, and you would access it in Julia using `model[:myvar]`, you can call
        `model.nvar("myvar")`.
        """
        try:
            return self.core[jl_symbol(var)]
        except Exception:
            raise Exception(f"Error while retrieving variable `{var}` from model")

    @staticmethod
    def _to_pylist(obj):
        # if isinstance(obj, jl.VectorValue):
        #    return jl.PythonCall.pylist(obj)
        return obj
