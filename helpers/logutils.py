import logging
from turtle import hideturtle

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def setup_logger(name, log_file, level=logging.INFO, overwrite=False):
    if overwrite:
        from os import remove, path

        if path.exists(log_file):
            remove(log_file)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


joblogger = setup_logger("joblogger", "job.log")
