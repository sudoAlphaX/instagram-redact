import configparser
import os


def importconfig(args):

    try:
        if os.path.isfile("config.ini"):
            config = configparser.ConfigParser()
            config.read("config.ini")
            return config[args]

        else:
            return None

    except:
        return None
