import sys

from instagrapi import Client

from helpers.configutils import get_config
from helpers.instautils import login
from helpers.logutils import clientlogger as logger

cl = login(Client())

silent_mode = get_config('logs', 'silent', False)

if cl is not None:
    if not silent_mode: print(f"Logged in to Instagram as: {(cl.account_info().dict())["username"]}")
    logger.info(f"Logged in to Instagram")

else:
    if not silent_mode: print("Failed to log in. Check client.log")
    logger.error(f"Failed to log in: {cl}")
    sys.exit(0)
