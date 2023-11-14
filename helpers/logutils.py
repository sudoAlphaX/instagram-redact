import logging

from helpers.configutils import read_config

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def newLogger(name, log_file, level="INFO", overwrite=False):
    """
    The newLogger function creates a new logger object with the given name and log file.
        The level parameter is optional, but if provided it will set the minimum logging level of the logger instead of INFO.
        If overwrite is True, then any existing log file will be overwritten.
        Refer https://docs.python.org/3/library/logging.html#logging-levels for logging level hierarchy.

    Args:
        name: Name the logger
        log_file: Specify the file that the logger will write to
        level: Set the minimum level of logging
        overwrite: Determine if the log file should be overwritten or not

    Returns:
        A logger object

    Doc Author:
        Trelent
    """

    loglevel = translateloglevel(level)

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


def consolelog(args, read=False, fallback=None):
    """
    The consolelog function is a wrapper for the print function.
    It allows you to use it in silent mode, where all output will be redirected to the log file instead of console.
    If read = True, then consolelog will return user input. If read = True but silent mode is enabled, the consolelog return the fallback.

    Args:
        args: Pass the message to be printed
        read: Determine whether the function is being used to print just print or also return user input
        fallback: Set a default value to return instead of user input if silent_mode is enabled

    Returns:
        The user input or fallback if silent mode is enabled

    Doc Author:
        Trelent
    """

    if not silent_mode:
        if not read:
            print(args)
            return True
        else:
            return input(args)

    else:
        if read:
            clientlogger.error(
                f"Silent Mode enabled. '{args}' input skipped. Used '{fallback}' instead"
            )
        return fallback


def translateloglevel(level):
    """
    The translateloglevel function takes a string as an argument and returns the corresponding logging level.

    Args:
        level: Define the level of logging as a string

    Returns:
        A logger level object

    Doc Author:
        Trelent
    """

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
    name="joblogger",
    log_file="job.log",
    level="INFO" if not read_config("logs", "debug", False) else "DEBUG",
)

clientlogger = newLogger(
    name="clientlogger",
    log_file="client.log",
    level="INFO" if not read_config("logs", "debug", False) else "DEBUG",
)

clientlogger.info("====================START====================")
