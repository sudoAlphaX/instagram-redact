import datetime
import json
import os
import pickle
import time

from instagrapi.exceptions import ChallengeRequired, FeedbackRequired

from helpers.configutils import read_config
from helpers.logutils import clientlogger, consolelog, joblogger


def format_export(file="export/liked_posts.json"):
    with open(file) as json_file:
        data = json.load(json_file)

    liked_medias_urls = []

    for liked_media in data["likes_media_likes"]:
        liked_medias_urls.append(
            {
                "url": liked_media["string_list_data"][0]["href"],
                "author": liked_media.get("title", "unknown"),
            }
        )

    os.rename(file, (os.path.dirname(file) + "/old_liked_posts.json"))

    return liked_medias_urls


def write_dump(var, file="temp/remaining_posts.dump"):
    if subdirectory := os.path.dirname(file):
        os.makedirs(subdirectory, exist_ok=True)

    with open(file, "wb") as dump_file:
        pickle.dump(var, dump_file)


def read_dump(file="temp/remaining_posts.dump"):
    clientlogger.debug("Attempt to read temp/remaining_posts.dump")

    with open(file, "rb") as dump_file:
        data = pickle.load(dump_file)

    return data


def get_liked_medias():
    if os.path.exists("temp/remaining_posts.dump"):
        return read_dump()

    else:
        if os.path.exists("export/liked_posts.json"):
            clientlogger.debug(
                "'export/liked_posts.json found'. Attempt to dump data to 'temp/remaining_posts.dump'"
            )
            write_dump(liked_medias := format_export())

            clientlogger.info(
                "Processed 'liked_posts.json' export file. Renaming to 'old_liked_posts.json'"
            )

            return liked_medias

        else:
            clientlogger.warn(
                "'liked_posts.json' not found in export directory. Paste the .json file. Read README for more help."
            )

            return []


pending_liked_medias = get_liked_medias()


def unlike_media(client):
    clientlogger.debug("Attempt to unlike %s posts", len(pending_liked_medias))  # type: ignore

    status = {"can_continue": True, "rate_limited": False, "jobs": []}

    for post in pending_liked_medias:  # type: ignore
        try:
            media_id = client.media_id(client.media_pk_from_url(post["url"]))
            client.media_unlike(media_id)

        except FeedbackRequired as e:
            clientlogger.error(f"Rate limited: {e}")
            status = {
                "can_continue": True,
                "rate_limited": True,
            }
            break

        except ChallengeRequired as e:
            clientlogger.error(
                "Rate limited: Complete captcha by logging in to web: %s", e
            )

            status = {
                "can_continue": False,
                "rate_limited": True,
            }
            break

        except Exception as e:
            clientlogger.error("Unexpected error: %s", e)
            status = {
                "can_continue": False,
                "rate_limited": False,
            }
            break

        else:
            joblogger.info(
                f"Unliked post {post['url']} by '{post['author']}'. Post id: {media_id}"
            )

            consolelog(f"Unliked {post['url']} by '{post['author']}'")

            pending_liked_medias.remove(post)  # type: ignore
            joblogger.debug("Removed %s from global list", post)

            clientlogger.debug("Dumping 'pending_liked_medias 'variable: Number of items: %s", len(pending_liked_medias))  # type: ignore
            write_dump(var=pending_liked_medias)

    return status


def unlike_all(client):
    status = {"can_continue": True, "rate_limited": False}
    completed = False
    unlike_retries = 0

    while status["can_continue"]:
        if status["rate_limited"]:
            # if len(status['jobs'] > 0):

            if unlike_retries >= int(read_config("ratelimit", "unlike_retries", 3)):  # type: ignore
                break

            while unlike_retries < int(
                read_config("ratelimit", "unlike_retries", 3)  # type: ignore
            ):  # max delay = 16 minutes
                clientlogger.warning(
                    "Rate limited: Pausing unlike requests for %s seconds. Resuming at %s",
                    (secs := (60 * (mins := int(read_config("ratelimit", "unlike_delay", 10)) * (unlike_retries + 1)))),  # type: ignore
                    (
                        resumetime := (
                            datetime.datetime.now() + datetime.timedelta(seconds=secs)
                        ).strftime("%H:%M:%S")
                    ),
                )

                consolelog(
                    args="Rate limited: Pausing unlike requests for %s minutes. Resuming at %s"
                    % (
                        mins,
                        resumetime,
                    )
                )

                time.sleep(secs)

                status = unlike_media(client)

                unlike_retries += 1

        else:
            if len(pending_liked_medias) > 0:  # type: ignore
                status = unlike_media(client)

            else:
                completed = True
                break

    return {
        "completed": completed,
        "can_continue": status["can_continue"],
        "rate_limited": status["rate_limited"],
    }
