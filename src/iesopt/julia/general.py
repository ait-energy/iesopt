import os
import importlib.metadata

from ..util import logger, set_iesopt_module_attr
from .setup import setup_julia, import_modules


def initialize():
    if os.getenv("IESOPT_DOCS_NOEXEC"):
        logger.warning("Detected docs environment (env. var. `IESOPT_DOCS_NOEXEC` is set), skip loading Julia")
        return

    logger.info("Integrated Energy System Optimization (IESopt)")
    logger.info("© 2021 - now:  AIT Austrian Institute of Technology GmbH")
    logger.info("Documentation: https://ait-energy.github.io/iesopt")

    juliacall = setup_julia()
    julia = juliacall.Main
    set_iesopt_module_attr("julia", julia)
    set_iesopt_module_attr("juliacall", juliacall)

    import_modules()
    logger.info("Versions: py=%s, jl=%s" % (importlib.metadata.version("iesopt"), str(julia.pkgversion(julia.IESopt))))

    set_iesopt_module_attr("IESopt", julia.IESopt)
    set_iesopt_module_attr("JuMP", julia.JuMP)

    set_iesopt_module_attr("jump_value", julia.seval("(x) -> JuMP.value.(x)"))
    set_iesopt_module_attr("jump_dual", julia.seval("(x) -> JuMP.dual.(x)"))
    set_iesopt_module_attr("jump_reduced_cost", julia.seval("(x) -> JuMP.reduced_cost.(x)"))
    set_iesopt_module_attr("jump_shadow_price", julia.seval("(x) -> JuMP.reduced_cost.(x)"))

    set_iesopt_module_attr("Docs.doc", julia.seval("(x) -> Docs.doc(x)"))

    return julia
