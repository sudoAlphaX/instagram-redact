from instagrapi.exceptions import ChallengeRequired, FeedbackRequired

from helpers.configutils import read_config
from helpers.logutils import clientlogger, consolelog, joblogger
from helpers.stringutils import str_to_bool

silent_mode = str_to_bool(read_config("logs", "silent", False))


def unlike_media(posts, client):
    """
    The unlike_media function takes in a list of posts and an Instagrapi client object.
    It then iterates through the list of posts, unliking each one. If it encounters
    an error, it will log that error and return False.

    Args:
        posts: Pass in the list of posts to unlike
        client: Authenticated Instagrapi Client object

    Returns:
        True if the media is unliked successfully or False if any error occurs

    Doc Author:
        Trelent
    """

    for post in posts:
        try:
            client.media_unlike(post.id)

        except FeedbackRequired as e:
            clientlogger.error(f"Rate limited: {e}")
            return False

        except ChallengeRequired:
            clientlogger.error("Rate limited: Complete captcha by logging in to web")
            return False

        except Exception as e:
            clientlogger.error("Unexpected error: %s", e)
            return False

        else:
            joblogger.info(
                f"Unliked post https://www.instagram.com/p/{post.code}/ by '{post.user.full_name}' (@{post.user.username}). Post id: {post.id}"
            )

            consolelog(
                f"Unliked https://www.instagram.com/p/{post.code}/ by '{post.user.full_name}' (@{post.user.username})"
            )

    return True


def unlike_all(client):
    """
    The unlike_all function is used to unlike all of the media that you have liked.
        This function will continue to unlike posts until there are no more posts left in your liked medias.

    Args:
        client: Instagrapi authenticated client object

    Doc Author:
        Trelent
    """

    status = True

    while (status is True) and (
        liked_medias := client.liked_medias(
            read_config("ratelimit", "max_fetch_count", 25)
        )
    ):
        joblogger.info(
            f"Fetching last {read_config('ratelimit', 'max_fetch_count', 25)} liked posts"
        )

        joblogger.debug(liked_medias)

        status = unlike_media(liked_medias, client)
