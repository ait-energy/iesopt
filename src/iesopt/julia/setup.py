import os
import ssl

from ..util.constants import JULIA_STATE, julia
from ..util.logging import logger


def setup_julia():
    """asdastgetwertfgdssd"""
    global JULIA_STATE, julia
    logger.info("Setting up Julia ...")

    # Check for local SSL certificate file, that can interfere with Julia setup.
    _ssl = None
    if "SSL_CERT_FILE" in os.environ:
        logger.info("Detected local `SSL_CERT_FILE`; disabling it during Julia setup")
        _ssl = os.environ.pop("SSL_CERT_FILE")

    ssl._create_default_https_context = ssl._create_unverified_context
    logger.warn("Disabling SSL verification to prevent problems; this may be unsafe")

    # Setup Julia (checking if it "looks" valid).
    import juliapkg
    if juliapkg.resolve() != True:
        JULIA_STATE = "invalid"
        raise Exception("Julia setup is not valid")

    import juliacall
    julia = juliacall.Main
    JULIA_STATE = "success"


if not os.getenv("IESOPT_DOCS_NOEXEC"):
    setup_julia()
else:
    logger.warn("Detected docs environment (env. var. `IESOPT_DOCS_NOEXEC` is set), skip loading Julia.")
    JULIA_STATE = "skipped"
