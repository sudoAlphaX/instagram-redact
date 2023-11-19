import datetime
import time

from instagrapi.exceptions import ChallengeRequired, FeedbackRequired

from helpers.configutils import read_config
from helpers.logutils import clientlogger, consolelog, joblogger


def unlike_media(posts, client, score=0):
    """
    The unlike_media function takes a list of posts, an Instagram client, and a score.
    It attempts to unlike each post in the list using the provided client. If it is successful,
    it removes that post from the unprocessed_posts list and logs its success to both joblogger
    and consolelog. It also decrements score by 1 if it is greater than 0 (to prevent negative scores).
    If there are any errors or exceptions during this process, they are logged with error level messages
    to both joblogger and consolelog. If it is rate limited, the score is incremented by 10.

    Args:
        posts: Pass the list of posts to unlike
        client: Pass the client object to the function
        score: Determine the rate limit delays

    Returns:
        A dictionary with the following keys: can_continue, rate_limited and score

    Doc Author:
        Trelent
    """

    clientlogger.debug("Attempt to unlike %s posts", len(posts))

    unprocessed_posts = posts
    status = {"can_continue": True, "rate_limited": False, "score": score}

    for post in posts:
        try:
            client.media_unlike(post.id)

        except FeedbackRequired as e:
            clientlogger.error(f"Rate limited: {e}")
            status = {"can_continue": True, "rate_limited": True, "score": score + 10}
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
            status["score"] = score - 1 if score > 0 else score

            unprocessed_posts.remove(post)

            joblogger.info(
                f"Unliked post https://www.instagram.com/p/{post.code}/ by '{post.user.full_name}' (@{post.user.username}). Post id: {post.id}"
            )

            consolelog(
                f"Unliked https://www.instagram.com/p/{post.code}/ by '{post.user.full_name}' (@{post.user.username})"
            )

    return status


def unlike_all(client, score=0):
    """
    The unlike_all function is used to unlike all of the posts that you have liked.
        It will return a status object with the following properties:
            completed - A boolean indicating whether or not it has finished unliking all of your posts.
            can_continue - A boolean indicating whether or not it can continue unliking your posts (if there are more).
            rate_limited - A boolean indicating if you have been rate limited by Instagram for liking too many times in a row.
                If this happens, wait until the next day and try again!

    Args:
        client: Pass the client object to the function
        score: Determine the rate limit delays

    Returns:
        A dictionary

    Doc Author:
        Trelent
    """

    status = {"can_continue": True, "rate_limited": False, "score": score}

    while status["can_continue"] and not status["rate_limited"]:
        joblogger.debug(
            "Fetching last {} liked posts".format(
                fetch_count := read_config("ratelimit", "max_fetch_count", 25),
            )
        )

        pending_liked_medias = client.liked_medias(fetch_count)

        if len(pending_liked_medias) > 0:
            joblogger.debug(pending_liked_medias)

            status = unlike_media(client, score)
            status["completed"] = False

        else:
            status = {
                "completed": True,
                "can_continue": False,
                "rate_limited": False,
                "score": score,
            }

    return status


def old_unlike_all(client):
    """
    The unlike_all function is used to unlike all of the posts that you have liked.
        This function will continue to run until there are no more posts left in your feed.
        The function will also pause for a period of time if it encounters an error from Instagram's API due to rate limiting.

    Args:
        client: Pass the client object to the function

    Returns:
        A dictionary with the following keys: completed, can_continue and rate_limited.

    Doc Author:
        Trelent
    """

    status = {"can_continue": True, "rate_limited": False, "jobs": []}
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

                status = unlike_media(status["jobs"], client)

                unlike_retries += 1

            # else:

            #     if (len(liked_medias := client.liked_medias(fetch_count := read_config("ratelimit", "max_fetch_count", 25))) > 0):

            #         clientlogger.info(f"Fetching last {fetch_count} liked posts")

            #         while unlike_retries < 5:  # max delay = 16 minutes
            #             clientlogger.warning(
            #                 "Rate limited: Pausing unlike requests for %s minutes",
            #                 (mins := (60 * (2 ^ unlike_retries))),
            #             )
            #             consolelog(args=("Rate limited: Pausing unlike requests for %s minutes", mins))
            #             time.sleep(mins)

            #             status = unlike_media(liked_medias, client)

            # else:
            #     return True

            # unlike_retries += 1

        else:
            joblogger.debug(
                "Fetching last {} liked posts".format(
                    fetch_count := read_config("ratelimit", "max_fetch_count", 25),
                )
            )

            joblogger.debug(liked_medias := client.liked_medias(fetch_count))

            if len(liked_medias) > 0:
                status = unlike_media(liked_medias, client)

            else:
                completed = True
                break

    return {
        "completed": completed,
        "can_continue": status["can_continue"],
        "rate_limited": status["rate_limited"],
    }

    # while liked_medias := client.liked_medias(
    #     read_config("ratelimit", "max_fetch_count", 25)
    # ):
    #     joblogger.info(
    #         f"Fetching last {read_config('ratelimit', 'max_fetch_count', 25)} liked posts"
    #     )

    #     clientlogger.info(
    #         f"Fetching last {read_config('ratelimit', 'max_fetch_count', 25)} liked posts"
    #     )

    #     joblogger.debug(liked_medias)

    #     while (jobs := unlike_media(liked_medias, client) is not None) and (
    #         len(jobs) > 0
    #     )(unlike_retries < 5):
    #         clientlogger.warning("Rate l")
    #         time.sleep(60 * (2 ^ unlike_retries))
    #         unlike_media(jobs, client)
