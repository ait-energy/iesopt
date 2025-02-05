import os
import sys
from pathlib import Path
import ssl

from ..util import logger
from .util import jl_import
from ..config import Config


def lookup_package(name: str):
    lookup = {
        "jump": ("JuMP", "4076af6c-e467-56ae-b986-b466b2749572"),
        "highs": ("HiGHS", "87dc4568-4c63-4d18-b0c0-bb2238e4078b"),
        "iesopt": ("IESopt", "ed3f0a38-8ad9-4cf8-877e-929e8d190fe9"),
        "gurobi": ("Gurobi", "2e9cd046-0924-5485-92f1-d5272153d98b"),
        "cplex": ("CPLEX", "a076750e-1247-5638-91d2-ce28b192dca0"),
        "ipopt": ("Ipopt", "b6b21f68-93f8-5de0-b562-5493be1d77c9"),
        "pythoncall": ("PythonCall", "6099a3de-0909-46bc-b1f4-468b9a2dfc0d"),
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
    target = str((Path(__file__).parent / "..").resolve())
    logger.info(f"    Target for juliapkg: '{target}'")

    logger.info("Checking Julia environment")

    if "juliacall" in sys.modules:
        logger.error(
            "It seems juliacall, and thus Julia, is already loaded; this may lead to unexpected behavior and prevents"
            " proper setup based on the internal configs. If you are sure this is not an issue, you can safely ignore"
            " this message, but we cannot guarantee anything to work as expected."
        )

    if Path("juliapkg.json").exists():
        raise Exception("Found `juliapkg.json` file; remove it to prevent potential conflicts")

    if (Path(__file__).parent / ".." / "juliapkg.json").exists():
        (Path(__file__).parent / ".." / "juliapkg.json").unlink()

    # Check for local SSL certificate file, that can interfere with Julia setup.
    _ssl = None
    if "SSL_CERT_FILE" in os.environ:
        logger.debug("Detected local `SSL_CERT_FILE`; disabling it during Julia setup")
        _ssl = os.environ.pop("SSL_CERT_FILE")

    ssl._create_default_https_context = ssl._create_unverified_context
    logger.info("Disabling SSL verification to prevent problems; this may be unsafe")

    # Set `JULIA_SSL_CA_ROOTS_PATH` to prevent various SSL related issues (with Julia setup; LibGit2; etc.).
    if "JULIA_SSL_CA_ROOTS_PATH" in os.environ:
        if os.environ["JULIA_SSL_CA_ROOTS_PATH"] != "":
            logger.info(
                "Overwriting the env. variable `JULIA_SSL_CA_ROOTS_PATH` (current: `%s`) to prevent SSL issues during the Julia setup"
                % str(os.environ["JULIA_SSL_CA_ROOTS_PATH"])
            )
            os.environ["JULIA_SSL_CA_ROOTS_PATH"] = ""
    else:
        logger.debug('Setting `JULIA_SSL_CA_ROOTS_PATH = ""` to prevent SSL issues during the Julia setup')
        os.environ["JULIA_SSL_CA_ROOTS_PATH"] = ""

    # Setup Julia (checking if it "looks" valid).
    import juliapkg

    # Set Julia version.
    juliapkg.require_julia(f"={Config.get('julia')}", target=target)
    # add_package(juliapkg.add, "pythoncall", "0.9.23", target)

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
    logger.info("    Executable: %s" % juliapkg.executable())
    logger.info("    Project: %s" % juliapkg.project())

    custom_packages = list(Config.find("PKG_"))
    if len(custom_packages) > 0:
        logger.info("Installing custom Julia packages")

        try:
            juliacall.Main.seval("import Pkg")
        except Exception as e:
            logger.error(f"Failed to import Julia `Pkg`: {e}")

        for entry in custom_packages:
            name = entry[4:]
            try:
                juliacall.Pkg.add(name=name, version=Config.get(entry))
            except Exception as e:
                logger.error(f"Failed to install custom package '{name}': {e}")

    # Restoring potential SSL certificate.
    if _ssl is not None:
        logger.debug("Restoring local `SSL_CERT_FILE`")
        os.environ["SSL_CERT_FILE"] = _ssl

    return juliacall


def import_modules():
    logger.info("Importing Julia modules:")
    jl_import("IESopt")
    jl_import("JuMP")
