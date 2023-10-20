import configparser
import os


def read_config(section, key=None, fallback=None):
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
