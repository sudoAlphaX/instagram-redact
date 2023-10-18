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

import logging

logger = logging.getLogger()

cl = Client()

if isfile("session.json"):
    session = cl.load_settings("session.json")  # type: ignore

    try:
        cl.set_settings(session)
        cl.login(tokens["username"], tokens["password"])

        try:
            cl.get_timeline_feed()

        except LoginRequired:
            logger.info("Session is invalid, need to login via username and password")

            old_session = cl.get_settings()

            # use the same device uuids across logins
            cl.set_settings({})
            cl.set_uuids(old_session["uuids"])

            cl.login(tokens["username"], tokens["passowrd"])

    except Exception as e:
        
        logger.info(f"Couldn't login user using session information: {e}")

else:
    
    try:
        logger.info(f"Attempting to login via username and password. username: {tokens["username"]}")
        
        if cl.login(tokens["username"], tokens["password"]):
            cl.dump_settings("session.json") # type: ignore
            
    except Exception as e:
        logger.info(f"Couldn't login user using username and password: {e}")


logger.info(f"Logged in to instagram as: {(cl.account_info().dict())["username"]}")
print(f"Logged in to instagram as: {(cl.account_info().dict())["username"]}")
