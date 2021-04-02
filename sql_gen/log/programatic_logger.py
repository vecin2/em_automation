import logging
import sys
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
LOG_FILE = "log.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = RotatingFileHandler(
        LOG_FILE,
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=2,
        encoding=None,
        delay=0,
    )
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough

    # logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False

    return logger
