import sys

from instagrapi import Client

from helpers.configutils import read_config
from helpers.instautils import login
from helpers.logutils import clientlogger as logger
from helpers.stringutils import str_to_bool

cl = login(Client())

silent_mode = str_to_bool(read_config('logs', 'silent', False))

if cl is not None:

    cl.delay_range = [1, 3]

    if not silent_mode: print(f"Logged in to Instagram as: {(cl.account_info().dict())["username"]}")

    logger.info(f"Logged in to Instagram")
    logger.debug(cl.account_info())

else:

    if not silent_mode: print("Failed to log in. Check client.log")

    logger.error(f"Failed to log in: {cl}")
    sys.exit(0)
