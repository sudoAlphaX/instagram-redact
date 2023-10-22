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
from helpers.logutils import consolelog


def get_credentials(username=True, password=True):
    tokens = {"username": "username", "password": "password"}

    if username is True:
        tokens["username"] = (
            u
            if ((u := read_config("credentials", "username")) is not None)
            else consolelog(
                "Enter your Instagram Username: ",
                read=True,
                fallback=tokens["username"],
            )
        )

    if password is True:
        tokens["password"] = (
            p
            if ((p := read_config("credentials", "password")) is not None)
            else consolelog(
                "Enter your Instagram password: ",
                read=True,
                fallback=tokens["password"],
            )
        )

    return tokens


def get_2fa_code():
    if tokens := (read_config("credentials", "auth")):
        otp = pyotp.TOTP(tokens.replace(" ", ""))

        try:
            return otp.now()

        except binascii.Error as e:
            logger.error("2fa secret error: %s", e)

    return str(consolelog("Enter your 2 factor authentication code: ", read=True))


def login(client, mfa=False):
    credentials = get_credentials()

    if os.path.isfile("session.json"):
        logger.info("Session file found, attempting to reuse session")

        try:
            client.load_settings("session.json")
            client.login(
                credentials["username"],
                credentials["password"],
                verification_code=(get_2fa_code() if mfa else ""),
            )
            client.get_timeline_feed()

        except LoginRequired as e:
            logger.info("Session invalid, attempt to create new session: %s", e)

            old_session = client.get_settings()
            logger.debug("Using session settings: %s", old_session)

            client.set_settings({})
            client.set_uuids(old_session["uuids"])
            client.relogin(
                credentials["username"],
                credentials["password"],
                verification_code=(get_2fa_code() if mfa else ""),
            )
            client.get_timeline_feed()
            client.dump_settings("session.json")

        except BadPassword as e:
            logger.error("Bad password: %s", e)
            client = None

        except TwoFactorRequired:
            logger.info("2 factor authentication enabled")

            client = login(client, mfa=True)
            client.get_timeline_feed()
            client.dump_settings("session.json")

        except ChallengeRequired as e:
            logger.error(
                "Rate limited: Complete captcha by using an official client: %s", e
            )
            client = None

        except Exception as e:
            logger.error("Exception raised: %s", e)
            client = None

    else:
        logger.info("Session file not found, attempt to create new session")

        try:
            client.login(
                credentials["username"],
                credentials["password"],
                verification_code=(get_2fa_code() if mfa else ""),
            )
            client.get_timeline_feed()
            client.dump_settings("session.json")

        except BadPassword as e:
            logger.error("Bad password: %s", e)
            client = None

        except TwoFactorRequired:
            logger.info("2 factor authentication enabled")

            try:
                client = login(client, mfa=True)
                client.get_timeline_feed()
                client.dump_settings("session.json")

            except Exception as e:
                logger.error("Exception raised in 2fa verification: %s", e)
                client = None

        except ChallengeRequired as e:
            logger.error(
                "Rate limited: Complete captcha by using an official client: %s", e
            )
            client = None

        except Exception as e:
            logger.error("Unknown Eeception raised: %s", e)
            client = None

    logger.debug(client)
    return client
