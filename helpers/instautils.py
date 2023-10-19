import binascii
import os

import pyotp
from instagrapi.exceptions import BadPassword, LoginRequired, TwoFactorRequired

from helpers.configutils import importconfig
from helpers.logutils import clientlogger as logger


def get_credentials():
    if tokens := importconfig("credentials"):
        return {"username": tokens["username"], "password": tokens["password"]}

    else:
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")

        return {"username": username, "password": password}


def get_2fa_code():
    if tokens := importconfig("credentials"):
        if tokens.get("auth"):
            otp = pyotp.TOTP(tokens["auth"].replace(" ", ""))

            try:
                return otp.now()

            except binascii.Error as e:
                logger.error(f"2fa secret error: {e}")

    return input("Enter your 2 factor authentication code: ")


def login(client, mfa=False):
    credentials = get_credentials()

    if os.path.isfile("session.json"):
        logger.debug("Session file found")

        try:
            client.load_settings("session.json")  # type: ignore
            client.login(
                credentials["username"],
                credentials["password"],
                verification_code=(get_2fa_code() if mfa else ""),
            )
            client.get_timeline_feed()

        except LoginRequired as e:
            logger.info(f"Session invalid, attempt to create new session: {e}")

            old_session = client.get_settings()

            client.set_settings({})
            client.set_uuids(old_session["uuids"])
            client.login(
                credentials["username"],
                credentials["password"],
                verification_code=(get_2fa_code() if mfa else ""),
            )
            client.get_timeline_feed()
            client.dump_settings("session.json")  # type: ignore

        except BadPassword as e:
            logger.error(f"Bad password: {e}")
            client = None

        except TwoFactorRequired:
            logger.info("2 factor authentication enabled")

            client = login(client, mfa=True)
            client.get_timeline_feed()
            client.dump_settings("session.json")  # type: ignore

        except Exception as e:
            logger.error(e)
            client = None

    else:
        logger.info("Session file missing, attempt to create new session")

        try:
            client.login(
                credentials["username"],
                credentials["password"],
                verification_code=(get_2fa_code() if mfa else ""),
            )
            client.get_timeline_feed()
            client.dump_settings("session.json")  # type: ignore

        except BadPassword as e:
            logger.error(f"Bad password: {e}")
            client = None

        except TwoFactorRequired:
            logger.info("2 factor authentication enabled")

            client = login(client, mfa=True)
            client.get_timeline_feed()
            client.dump_settings("session.json")  # type: ignore

        except Exception as e:
            logger.error(e)
            client = None

    logger.debug(client)
    return client
