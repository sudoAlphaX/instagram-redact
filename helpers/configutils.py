import configparser
import os

from helpers.stringutils import str_to_bool

if os.path.isfile("config.ini"):
    config = configparser.ConfigParser()
    config.read("config.ini")

else:
    config = None


def read_config(section, key, fallback=None):
    """
    The read_config function reads the config.ini file and returns a boolean value
    based on the section and key provided. If no config file is found, or if the
    section/key does not exist in the config file, then it will return True by default.

    Args:
        section: Specify the section of the config file to read from
        key: Specify the key in the config file
        fallback: Return a set value if the key is not found in the config file

    Returns:
        A boolean value

    Doc Author:
        Trelent
    """

    global config

    if config is not None:
        if str_to_bool(
            config.get(section=section, option="debug", fallback=False)
        ):  # If in debug mode, read the file for every access to change values during runtime
            config = configparser.ConfigParser()
            config.read("config.ini")

        return (
            (
                str_to_bool(
                    config.get(section=section, option=key, fallback=fallback),
                    fallback=True,
                )
            )
            if section in config.sections()
            else fallback
        )

    else:
        return fallback


def read_section(section, fallback={}):
    """
    The read_section function reads the config.ini file and returns a dictionary of the keys of section specified in the first argument.
    If no such section exists, it will return an empty dictionary.

    Args:
        section: Specify the section in the config
        fallback: Set default values for the parameters in case they are not found in the config

    Returns:
        A dictionary of the section in config

    Doc Author:
        Trelent
    """

    global config

    if config is not None:
        if str_to_bool(
            config.get(section=section, option="debug", fallback=False)
        ):  # If in debug mode, read the file for every config read request to change values during runtime
            config = configparser.ConfigParser()
            config.read("config.ini")

        return dict((config[section])) if section in config.sections() else fallback

    else:
        return fallback


def edit_config(section, key, value):
    """
    The edit_config function takes three arguments:
        section - the section of the config file to edit
        key - the key in that section to edit
        value - what you want to set that key equal to

    Args:
        section: Specify the section in the config file
        key: Specify the key of the value you want to change
        value: Set the value of a key

    Returns:
        True if the file exists and false if it doesn't

    Doc Author:
        Trelent
    """

    if config is not None:
        config.set(section, key, value)

        with open("config.ini", "w") as configfile:
            config.write(configfile)

        return True

    else:
        return False
