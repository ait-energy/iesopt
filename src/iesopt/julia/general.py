import os
import importlib.metadata

from ..util import logger, set_iesopt_module_attr, get_iesopt_module_attr
from .setup import setup_julia, import_modules


def log_welcome_msg():
    julia = get_iesopt_module_attr("julia")
    version_core = str(julia.pkgversion(julia.IESopt))
    version_py = importlib.metadata.version("iesopt")
    version_lib = str(julia.pkgversion(julia.IESoptLib))
    n_v = max(len(version_core), len(version_py), len(version_lib))
    url_docs = "https://ait-energy.github.io/iesopt"

    def _fill(_s: str, n: int):
        return " " * (n - len(_s))

    logger.info("╔════════════════════════════════════════════════════════════════════════╗")
    logger.info("║            IESopt   «Integrated Energy System Optimization»            ║")
    logger.info("╟────────────────────────────────────────────────────────────────────────╢")
    logger.info("║   ╭────────────────────────────────────────────────────────────────╮   ║")
    logger.info("║   ├ authors: Stefan Strömer, Daniel Schwabeneder, and contributors │   ║")
    logger.info("║   ├ ©  2021: AIT Austrian Institute of Technology GmbH             │   ║")
    logger.info(f"║   ├    docs: {url_docs}{_fill(url_docs, 53)} │   ║")
    logger.info("║   ├ version: ┐                                                     │   ║")
    logger.info(f"║   │          ├─{{ py  :: {version_py}{_fill(version_py, n_v)} }} {' ' * 32} │   ║")
    logger.info(f"║   │          ├─{{ jl  :: {version_core}{_fill(version_core, n_v)} }} {' ' * 32} │   ║")
    logger.info(f"║   │          └─{{ lib :: {version_lib}{_fill(version_lib, n_v)} }} {' ' * 32} │   ║")
    logger.info("║   ╰────────────────────────────────────────────────────────────────╯   ║")
    logger.info("╚════════════════════════════════════════════════════════════════════════╝")


def initialize():
    if os.getenv("IESOPT_DOCS_NOEXEC"):
        logger.warn("Detected docs environment (env. var. `IESOPT_DOCS_NOEXEC` is set), skip loading Julia.")
        return

    julia = setup_julia()
    set_iesopt_module_attr("julia", julia)

    import_modules()
    log_welcome_msg()

    set_iesopt_module_attr("IESopt", julia.IESopt)
    set_iesopt_module_attr("JuMP", julia.JuMP)

    set_iesopt_module_attr("jump_value", julia.seval("(x) -> JuMP.value.(x)"))
    set_iesopt_module_attr("jump_dual", julia.seval("(x) -> JuMP.dual.(x)"))
    set_iesopt_module_attr("jump_reduced_cost", julia.seval("(x) -> JuMP.reduced_cost.(x)"))
    set_iesopt_module_attr("jump_shadow_price", julia.seval("(x) -> JuMP.reduced_cost.(x)"))

    return julia
