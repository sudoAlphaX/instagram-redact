import binascii
import os
import random
import time

import pyotp
from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    RecaptchaChallengeForm,
    ReloginAttemptExceeded,
    SelectContactPointRecoveryForm,
    TwoFactorRequired,
)
from instagrapi.mixins.challenge import ChallengeChoice

from helpers.configutils import edit_config, read_config
from helpers.logutils import clientlogger as logger
from helpers.logutils import consolelog, newLogger, silent_mode
from helpers.stringutils import str_to_bool


def get_credentials(username=True, password=True):
    """
    The get_credentials function is used to retrieve the username and password of an Instagram account either from config.ini or from the user.

    Args:
        username: Determine whether or not to prompt the user for a username
        password: Determine whether or not to prompt the user for a password

    Returns:
        A dictionary with the username and password

    Doc Author:
        Trelent
    """

    tokens = {"username": "username", "password": "password"}

    if username is True:
        tokens["username"] = (  # type: ignore
            u
            if ((u := read_config("credentials", "username")) is not None)
            else consolelog(
                "Enter your Instagram Username: ",
                read=True,
                fallback=tokens["username"],
            )
        )

    if password is True:
        tokens["password"] = (  # type: ignore
            p
            if ((p := read_config("credentials", "password")) is not None)
            else consolelog(
                "Enter your Instagram password: ",
                read=True,
                fallback=tokens["password"],
            )
        )

    logger.debug("Used username: %s", tokens["username"])

    return tokens


def get_2fa_code():
    """
    The get_2fa_code function is used to generate the 2 factor authentication code from 2fa secret in config.ini or prompt user for 2fa code.

    Returns:
        2 factor authentication code

    Doc Author:
        Trelent
    """

    if tokens := (read_config("credentials", "auth")):
        otp = pyotp.TOTP(tokens.replace(" ", ""))  # type: ignore

        try:
            return otp.now()

        except binascii.Error as e:
            logger.error("2fa secret error: %s", e)

    if not silent_mode:
        logger.info("Prompting for 2fa code")

        while True:
            code = consolelog(
                "Enter your 2 factor authentication code: ", read=True, fallback=None
            )

            if code and code.isdigit():  # type: ignore
                return code

    else:
        logger.critical(
            "2fa code required. Save 2fa secret in config.ini or disable silent_mode and enter the 2fa code"
        )
        return None


def get_code_from_sms(username):
    """
    The get_code_from_sms function is used to prompt the user for the 6 digit code sent as an SMS.

    Args:
        username: Username of the Instagram account to display

    Returns:
        The code sent to the user's phone number

    Doc Author:
        Trelent
    """

    if not silent_mode:
        logger.info("Prompting for verification code sent to SMS for: %s", username)

        while True:
            code = consolelog(
                f"Enter the 6 digits code sent to your SMS for {username}: ",
                read=True,
                fallback=None,
            )

            if code and code.isdigit():  # type: ignore
                return code
    else:
        logger.critical(
            "Rate limited: Disable silent_mode and enter the 6 digit code sent to you as an SMS for %s",
            username,
        )
        return None


def challenge_code_handler(username, choice):
    """
    The challenge_code_handler function is called when the user has to enter a code sent by SMS or Email.
    The function should return the code as string, or None if it could not be retrieved.

    Args:
        username: Identify the user for which a challenge is requested
        choice: Determine whether the user has received the code via SMS or Email

    Returns:
        Verification code as a string or None

    Doc Author:
        Trelent
    """

    if choice == ChallengeChoice.SMS:
        logger.info("Challenge choice SMS for username: %s", username)
        return get_code_from_sms(username)

    elif choice == ChallengeChoice.EMAIL:
        logger.info("Challenge choice Email for username: %s", username)
        return None

    else:
        logger.warning("Unknown challenge choice '%s' for %s", choice, username)
        return None


passwordlogger = newLogger(
    name="passwordlogger", level="INFO", log_file="passwords.log"
)


def change_password_handler(username):
    """
    The change_password_handler function is called when the client has been rate limited.
    It will either automatically generate a new password, or prompt the user for one.

    Returns:
        A password

    Doc Author:
        Trelent
    """

    if str_to_bool(read_config("ratelimit", "auto_change_password", False)):
        logger.warning(
            "Rate limited. Attempting to change password for username: %s", username
        )

        chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@")

        password = "".join(random.sample(chars, 10))

        if str_to_bool(read_config("ratelimit", "log_new_password", False)):
            passwordlogger.info("New password: %s", password)

    else:
        logger.warning("Rate limited: Prompting for new password")

        password = consolelog(
            (
                "Rate limited, enter a new password to be set for username %s (Use a strong password to avoid errors): ",
                username,
            ),
            read=True,
            fallback=None,
        )

    if password:
        edit_config("credentials", "password", password)

    return password


def login(client=Client(), mfa=False, relogin_delay=1, relogin_attempt=0):
    client.challenge_code_handler = challenge_code_handler  # type: ignore
    client.change_password_handler = change_password_handler  # type: ignore

    if os.path.isfile("session.json"):
        logger.info("Session found. Attempt to reuse session")

        client.load_settings("session.json")  # type: ignore

        try:
            tokens = get_credentials(False, False)
            client.login(tokens["username"], tokens["password"])
            client.get_timeline_feed()

        except LoginRequired as e:
            logger.warning("Invalid session: %s", e)

            old_session = client.get_settings()
            client.set_settings({})
            client.set_uuids(old_session["uuids"])

        except Exception as e:
            logger.warning("Error in reusing session: %s", e)
            client.set_settings({})

        else:
            logger.info(
                "Session valid. Logged in to Instagram as: %s",
                (client.account_info().dict()).get("username"),
            )
            return client

    tokens = get_credentials()

    try:
        client.login(tokens["username"], tokens["password"], verification_code=(get_2fa_code() if mfa else ""))  # type: ignore
        client.get_timeline_feed()

    except BadPassword as e:
        if relogin_attempt > 1:
            logger.error("Bad Password (Possibly Instagram IP Blacklist): %s", e)
            return None

        else:
            logger.error("Bad Password: %s", e)
            client = login(client, relogin_attempt=(relogin_attempt + 1))

    except LoginRequired as e:
        logger.warning("Login Required exception. Attempt relogin: %s", e)
        client.relogin()

    except TwoFactorRequired as e:
        logger.debug("2fa enabled, attempt to retrieve 2fa code: %s", e)
        client = login(client, mfa=True)

    except PleaseWaitFewMinutes as e:
        logger.warning("Rate limited. Pausing for 5 minutes before relogin: %s", e)
        consolelog(f"Rate limited. Pausing for 5 minutes: {e}")

        time.sleep(300)

        logger.info("Resuming login attempt")
        client = login(client)

    except ReloginAttemptExceeded as e:
        logger.critical("Relogin attempt exceeded: %s", e)
        client = None

    except FeedbackRequired as e:
        if (
            "Your account has been temporarily blocked"
            in client.last_json["feedback_message"]
        ):
            logger.critical(
                "Rate limited: %s; %s", e, client.last_json["feedback_message"]
            )

            return None

        else:
            logger.error("Rate limited. Retrying in %d hours: %s", relogin_delay, e)
            consolelog(f"Retrying in {relogin_delay} hours: {e}")

            time.sleep(3600 * relogin_delay)

            logger.info("Resuming login attempt")

            relogin_delay += 1
            client = login(client, relogin_delay=relogin_delay)

    except ChallengeRequired as e:
        logger.warning("Rate limited. Attempt to resolve challenge: %s", e)

        try:
            client.challenge_resolve(client.last_json)
            client.get_timeline_feed()

        except Exception as e:
            logger.critical("Failed to resolve challenge: %s", e)
            return None

        else:
            return client

    else:
        return client

    return client
