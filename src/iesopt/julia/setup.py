# import os
# import ssl

from ..util import logger
from .util import jl_import


def setup_julia():
    logger.info("Setting up Julia ...")

    # # Check for local SSL certificate file, that can interfere with Julia setup.
    # _ssl = None
    # if "SSL_CERT_FILE" in os.environ:
    #     logger.info("Detected local `SSL_CERT_FILE`; disabling it during Julia setup")
    #     _ssl = os.environ.pop("SSL_CERT_FILE")

    # ssl._create_default_https_context = ssl._create_unverified_context
    # logger.warn("Disabling SSL verification to prevent problems; this may be unsafe")

    # Setup Julia (checking if it "looks" valid).
    import juliapkg

    if not juliapkg.resolve():
        raise Exception("Julia setup is not valid")

    import juliacall

    logger.info("Julia setup successful")

    # # Restoring potential SSL certificate.
    # if _ssl is not None:
    #     logger.info("Restoring local `SSL_CERT_FILE`")
    #     os.environ["SSL_CERT_FILE"] = _ssl

    return juliacall.Main


def import_modules():
    jl_import("IESoptLib")
    jl_import("IESopt")
    jl_import("JuMP")
