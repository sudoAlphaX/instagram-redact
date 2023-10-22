import configparser
import os


def read_config(section, key=None, fallback=None):
    """
    The read_config function reads the config.ini file and returns a key
        from the specified section and key, or all keys in that section if no
        key is provided. If no config file exists, it will return None by default.

    Args:
        section: Specify the section of the config file to read from
        key: Get a specific key from the config file
        fallback: Set a default value if the config file is not found or the section/key does not exist

    Returns:
        key as string or all keys of a section as a dict

    Doc Author:
        Trelent
    """

    param = fallback

    if os.path.isfile("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")

        if key:
            param = (
                (config.get(section=section, option=key, fallback=fallback))
                if section in config.sections()
                else fallback
            )
        else:
            param = (
                dict((config[section])) if section in config.sections() else fallback
            )

    return param
