import os
import sys
from pathlib import Path
# import ssl

from ..util import logger
from .util import jl_import, jl_safe_seval
from ..config import Config


def lookup_package(name: str):
    lookup = {
        "jump": ("JuMP", "4076af6c-e467-56ae-b986-b466b2749572"),
        "highs": ("HiGHS", "87dc4568-4c63-4d18-b0c0-bb2238e4078b"),
        "iesopt": ("IESopt", "ed3f0a38-8ad9-4cf8-877e-929e8d190fe9"),
        "gurobi": ("Gurobi", "2e9cd046-0924-5485-92f1-d5272153d98b"),
        "cplex": ("CPLEX", "a076750e-1247-5638-91d2-ce28b192dca0"),
    }

    if name in lookup:
        return lookup[name]

    raise Exception(f"Failed to lookup Julia package '{name}'; please report this issue")


def add_package(f_add, name: str, config: str, target: str):
    if "github" in config:
        if "#" in config:
            url, rev = config.split("#")
            f_add(*lookup_package(name), url=url, rev=rev, target=target)
        else:
            f_add(*lookup_package(name), url=config, target=target)
    else:
        f_add(*lookup_package(name), version="=" + config, target=target)


def setup_julia():
    logger.info("Checking Julia environment")

    if "juliacall" in sys.modules:
        logger.error(
            "It seems juliacall, and thus Julia, is already loaded; this may lead to unexpected behavior and prevents"
            " proper setup based on the internal configs. If you are sure this is not an issue, you can safely ignore"
            " this message, but we cannot guarantee anything to work as expected."
        )

    if Path("juliapkg.json").exists():
        logger.warning("Found `juliapkg.json` file; removing it to prevent potential conflicts")
        Path("juliapkg.json").unlink()

    # # Check for local SSL certificate file, that can interfere with Julia setup.
    # _ssl = None
    # if "SSL_CERT_FILE" in os.environ:
    #     logger.info("Detected local `SSL_CERT_FILE`; disabling it during Julia setup")
    #     _ssl = os.environ.pop("SSL_CERT_FILE")

    # ssl._create_default_https_context = ssl._create_unverified_context
    # logger.warn("Disabling SSL verification to prevent problems; this may be unsafe")

    # Setup Julia (checking if it "looks" valid).
    import juliapkg

    target = str((Path(__file__).parent / "..").resolve())
    logger.info(f"Using temporary target for juliapkg: '{target}'")

    # Set Julia version.
    juliapkg.require_julia(f"={Config.get('julia')}", target=target)

    # Set versions of "core" packages.
    add_package(juliapkg.add, "jump", Config.get("jump"), target)
    add_package(juliapkg.add, "iesopt", Config.get("core"), target)

    # Set versions of "solver" packages.
    for entry in Config.find("solver_"):
        name = entry[7:]
        add_package(juliapkg.add, name, Config.get(entry), target)

    if not juliapkg.resolve(dry_run=True):
        logger.warning("The Julia environment is dirty and needs to be resolved, which can take some time")
        if not juliapkg.resolve(dry_run=False):
            raise Exception("Julia setup is not valid")

    logger.info("Julia environment ready, loading Julia")

    os.environ["JULIA_PKG_PRESERVE_TIERED_INSTALLED"] = "true"
    os.environ["PYTHON_JULIACALL_STARTUP_FILE"] = "no"
    os.environ["PYTHON_JULIACALL_AUTOLOAD_IPYTHON_EXTENSION"] = "no"

    if Config.get("multithreaded"):
        os.environ["PYTHON_JULIACALL_THREADS"] = "auto"
        os.environ["PYTHON_JULIACALL_HANDLE_SIGNALS"] = "yes"
    else:
        os.environ["PYTHON_JULIACALL_THREADS"] = "1"
        os.environ["PYTHON_JULIACALL_HANDLE_SIGNAL"] = "no"

    opt = Config.get("optimization")
    if opt == "rapid":
        os.environ["PYTHON_JULIACALL_COMPILE"] = "min"
        os.environ["PYTHON_JULIACALL_OPTIMIZE"] = "0"
        os.environ["PYTHON_JULIACALL_MIN_OPTLEVEL"] = "0"
    elif opt == "latency":
        os.environ["PYTHON_JULIACALL_COMPILE"] = "yes"
        os.environ["PYTHON_JULIACALL_OPTIMIZE"] = "0"
        os.environ["PYTHON_JULIACALL_MIN_OPTLEVEL"] = "0"
    elif opt == "default":
        pass
    elif opt == "performance":
        os.environ["PYTHON_JULIACALL_COMPILE"] = "all"
        os.environ["PYTHON_JULIACALL_OPTIMIZE"] = "3"
        os.environ["PYTHON_JULIACALL_MIN_OPTLEVEL"] = "3"
    else:
        raise Exception(f"Unknown optimization setting '{opt}'")

    import juliacall

    logger.info("Julia setup complete")

    custom_packages = list(Config.find("pkg_"))
    if len(custom_packages) > 0:
        logger.info("Installing custom Julia packages")
        jl_import("Pkg")
        for entry in custom_packages:
            name = entry[4:]
            jl_safe_seval(f"Pkg.add(Pkg.{name})")

    # # Restoring potential SSL certificate.
    # if _ssl is not None:
    #     logger.info("Restoring local `SSL_CERT_FILE`")
    #     os.environ["SSL_CERT_FILE"] = _ssl

    return juliacall


def import_modules():
    jl_import("IESopt")
    jl_import("JuMP")
