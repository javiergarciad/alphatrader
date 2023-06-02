import logging
import os
from pathlib import Path
import time
import logging.config
import yaml

from src.common.tools import get_project_root


logger = logging.getLogger(__name__)


class ErrorFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        return (
            record.levelno == logging.WARNING
            or record.levelno == logging.ERROR
            or record.levelno == logging.CRITICAL
        )


class InfoFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        return record.levelno == logging.INFO


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


def logging_setup():
    """Setup logging configuration"""

    config_filepath = Path(get_project_root(), "src/common", "logging_config.yml")

    # load the configuration file
    try:
        with open(config_filepath, "rt") as f:
            config = yaml.safe_load(f.read())
    except Exception as e:
        logger.critical(f"Unable to open '{config_filepath}", exc_info=True)
        raise SystemExit

    try:
        # Configure the logging module with the config file
        logging.config.dictConfig(config)
        logger.debug("Logging configured")
    except Exception as e:
        logger.critical(f"Unable to load config: '{config_filepath}", exc_info=True)
        raise SystemExit


if __name__ == "__main__":
    logging_setup()
    logger = logging.getLogger(__name__)

    # Some examples.
    logger.debug("this is a debugging message")
    logger.info("this is an informational message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")
    logger.critical("this is a critical message")
