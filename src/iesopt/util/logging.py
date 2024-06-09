import logging


def setup_logger():
    logging.basicConfig()
    logger = logging.getLogger("iesopt")
    logger.setLevel(logging.DEBUG)
    return logger


logger = setup_logger()
