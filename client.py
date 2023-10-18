import os

configpresent = bool(os.path.exists("config.ini"))

if not configpresent:
    sampleconfig = open("sampleconfig.ini", "r").read()

    configtext = sampleconfig.format(
        username=os.environ.get("username"), password=os.environ.get("password")
    )

    with open("config.ini", "w") as configfile:
        configfile.write(configtext)


import configparser

config = configparser.ConfigParser()
config.read("config.ini")
tokens = config["credentials"]


from instagrapi import Client
from instagrapi.exceptions import LoginRequired

from os.path import isfile

from helpers import logutils

clientlogger = logutils.setup_logger('clientlogger', 'client.log')
cl = Client()
cl.delay_range = [1, 3]

if isfile("session.json"):
    
    session = cl.load_settings("session.json")  # type: ignore
    clientlogger.info("Session file found, using Session file")

    try:
        cl.set_settings(session)
        cl.login(tokens["username"], tokens["password"])

        try:
            cl.get_timeline_feed()

        except LoginRequired:
            clientlogger.info("Session is invalid, recreating session file")

            from os import remove

            remove("session.json")

            cl.login(tokens["username"], tokens["password"])
            cl.dump_settings("session.json")  # type: ignore

    except Exception as e:
        clientlogger.error("Couldn't login user using session information: %s" % e)

else:
    clientlogger.info("Session not found, creating session file")

    cl.login(tokens["username"], tokens["password"])
    cl.dump_settings("session.json")  # type: ignore

    try:
        cl.get_timeline_feed()

    except Exception as e:
        clientlogger.error("Couldn't login user using login information: %s" % e)

print(f"Logged in to instagram as: {(cl.account_info().dict())["username"]}")
