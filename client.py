import sys

from instagrapi import Client

from helpers.instautils import login
from helpers.logutils import clientlogger as logger
from helpers.logutils import consolelog

cl = login(Client())

if cl is not None:
    cl.delay_range = [1, 3]

    consolelog(
        f"Logged in to Instagram as: {(cl.account_info().dict()).get('username')}"
    )

    logger.info("Logged in to Instagram")
    logger.debug(cl.account_info())

else:
    consolelog("Failed to log in. Check client.log")

    logger.error("Failed to log in")
    sys.exit(0)
