import logging

from helpers.configutils import read_config
from helpers.stringutils import str_to_bool

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def newLogger(name, log_file, level="INFO", overwrite=False):
    loglevel = translatelevel(level)

    if overwrite:
        from os import path, remove

        if path.exists(log_file):
            remove(log_file)

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    logger.addHandler(handler)

    return logger


silent_mode = read_config("logs", "silent", False)


def translatelevel(level):
    if level == "INFO":
        loglevel = logging.INFO
    elif level == "DEBUG":
        loglevel = logging.DEBUG
    elif level == "WARNING":
        loglevel = logging.WARNING
    elif level == "ERROR":
        loglevel = logging.ERROR
    elif level == "CRITICAL":
        loglevel = logging.CRITICAL
    else:
        raise Exception("Undefined log level")

    return loglevel


joblogger = newLogger(
    "joblogger",
    "job.log",
    "INFO" if not str_to_bool(read_config("logs", "debug", False)) else "DEBUG",
)

clientlogger = newLogger(
    "clientlogger",
    "client.log",
    "INFO" if not str_to_bool(read_config("logs", "debug", False)) else "DEBUG",
)
