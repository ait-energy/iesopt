import os
import importlib.metadata
from pathlib import Path
import tempfile

# Set version.
__version__ = importlib.metadata.version("iesopt")

# Set juliapkg target path.
__target__ = Path(tempfile.mkdtemp(prefix="iesopt"))
__target__.mkdir(exist_ok=True)
try:
    _pre_295_target = (Path().cwd() / ".iesopt" / "juliapkg.json").resolve()
    if _pre_295_target.exists():
        print(
            "WARNING: Found an old `juliapkg.json` file from previous version of `iesopt`, removing it to prevent potential"
            " conflicts; you should only see this warning once after upgrading"
        )
        _pre_295_target.unlink()
except Exception as e:
    print(f"WARNING: Failed to remove old `juliapkg.json` file: {e}")

# Set sysimage path.
__sysimage__ = Path().cwd() / ".iesopt" / ("sysimage_v" + __version__.replace(".", "-") + ".so")

# =======================================================================
# Setup "module globals" that will be overwritten internally.
julia = None
"""
The Julia object, if setup was successful.

..  code-block:: python
    :caption: Usage

    import iesopt
    iesopt.julia.println("Hello, from Julia's world!")
"""

Symbol = None

IESopt = None
"""IESopt.jl module from Julia."""

JuMP = None
"""JuMP.jl module from Julia."""


def jump_value(item):
    """Calls `JuMP.value.(item)`."""
    pass


def jump_dual(item):
    """Calls `JuMP.dual.(item)`."""
    pass


def jump_reduced_cost(item):
    """Calls `JuMP.reduced_cost.(item)`."""
    pass


def jump_shadow_price(item):
    """Calls `JuMP.shadow_price.(item)`."""
    pass


def get_jl_docstr(obj: str):
    """Get the documentation string of a Julia object inside the IESopt module."""
    pass


# =======================================================================

# Setup Julia.
from .julia import initialize as _initialize_everything  # noqa: E402
from .util import get_iesopt_module_attr as _get_iesopt_module_attr  # noqa: E402

julia = _initialize_everything(__target__, __sysimage__)

# Export everything.
from iesopt.model import Model as Model, ModelStatus as ModelStatus  # noqa: E402
from iesopt.results import Results as Results  # noqa: E402
from iesopt.iesopt import run as run, examples as examples, make_example as make_example  # noqa: E402

from .julia.util import jl_symbol as jl_symbol, jl_docs  # noqa: E402
from .julia import jl_isa as jl_isa  # noqa: E402

Symbol = jl_symbol

if not os.getenv("IESOPT_DOCS_NOEXEC"):
    IESopt = _get_iesopt_module_attr("IESopt")
    JuMP = _get_iesopt_module_attr("JuMP")

    jump_value = _get_iesopt_module_attr("jump_value")
    jump_dual = _get_iesopt_module_attr("jump_dual")
    jump_reduced_cost = _get_iesopt_module_attr("jump_reduced_cost")
    jump_shadow_price = _get_iesopt_module_attr("jump_shadow_price")
    get_jl_docstr = jl_docs


def create_sysimage():
    """Create a sysimage containing IESopt.jl and important dependencies."""
    import juliacall
    import juliapkg

    julia.Pkg.add("PackageCompiler")
    julia.seval("import PackageCompiler")

    __target__.mkdir(exist_ok=True)

    juliapkg.add("Pkg", "44cfe95a-1eb2-52ea-b672-e2afdf69b78f", target=str(__target__ / "juliapkg.json"))
    juliapkg.resolve()

    julia.PackageCompiler.create_sysimage(
        juliacall.convert(julia.Vector, ["IESopt", "JuMP", "HiGHS", "Pkg"]), sysimage_path=str(__sysimage__)
    )

    print("Successfully created sysimage; launch your script/code again to use it")
    exit(0)
