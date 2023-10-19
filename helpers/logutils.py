import logging

from helpers.configutils import importconfig
from helpers.stringutils import str_to_bool

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def newLogger(name, log_file, level="INFO", overwrite=False):
    loglevel = translatelevel(level)

    if overwrite:
        from os import path, remove

        if path.exists(log_file):
            remove(log_file)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    logger.addHandler(handler)

    return logger


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


logconfig = importconfig("logs")


joblogger = newLogger(
    "joblogger",
    "job.log",  # type: ignore
    "INFO"
    if ((q := importconfig("logs")) == None)
    else ("DEBUG" if str_to_bool(q.get("debug")) else "INFO"),  # type: ignore
)

clientlogger = newLogger(
    "clientlogger",
    "client.log",
    "INFO"
    if ((q := importconfig("logs")) == None)
    else ("DEBUG" if str_to_bool(q.get("debug")) else "INFO"),  # type: ignore
)
