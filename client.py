from instagrapi import Client

from helpers.instautils import login
from helpers.logutils import clientlogger as logger

cl = login(Client())

if cl:
    print(f"Logged in to Instagram as: {(cl.account_info().dict())["username"]}")
    logger.info(f"Logged in to Instagram")

else:
    print("Failed to log in. Check client.log")
    logger.error(f"Failed to log in: {cl}")
