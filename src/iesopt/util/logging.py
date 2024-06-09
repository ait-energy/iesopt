import logging


def setup_logger():
    logger = logging.getLogger("iesopt")
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()
