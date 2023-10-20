import binascii
import os

import pyotp
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    LoginRequired,
    TwoFactorRequired,
)

from helpers.configutils import read_config
from helpers.logutils import clientlogger as logger


def get_credentials(username=True, password=True):
    tokens = {"username": "username", "password": "password"}

    if username is True:
        tokens["username"] = (
            u
            if ((u := read_config("credentials", "username")) is not None)
            else input("Enter your Instagram username: ")
        )
    if password is True:
        tokens["password"] = (
            p
            if ((p := read_config("credentials", "password")) is not None)
            else input("Enter your Instagram password : ")
        )

    return tokens


def get_2fa_code():
    if tokens := (read_config("credentials", "auth")):
        otp = pyotp.TOTP(tokens.replace(" ", ""))

        try:
            return otp.now()

        except binascii.Error as e:
            logger.error(f"2fa secret error: {e}")

    return int(input("Enter your 2 factor authentication code: "))


def login(client, mfa=False):
    credentials = get_credentials()

    if os.path.isfile("session.json"):
        logger.debug("Session file found")

        try:
            client.load_settings("session.json")
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
            client.dump_settings("session.json")

        except BadPassword as e:
            logger.error(f"Bad password: {e}")
            client = None

        except TwoFactorRequired:
            logger.info("2 factor authentication enabled")

            client = login(client, mfa=True)
            client.get_timeline_feed()
            client.dump_settings("session.json")

        except ChallengeRequired as e:
            logger.error(
                f"Rate limited: Complete captcha by using an official client: {e}"
            )
            client = None

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
            client.dump_settings("session.json")

        except BadPassword as e:
            logger.error(f"Bad password: {e}")
            client = None

        except TwoFactorRequired:
            logger.info("2 factor authentication enabled")

            client = login(client, mfa=True)
            client.get_timeline_feed()
            client.dump_settings("session.json")

        except ChallengeRequired as e:
            logger.error(
                f"Rate limited: Complete captcha by using an official client: {e}"
            )
            client = None

        except Exception as e:
            logger.error(e)
            client = None

    logger.debug(client)
    return client
