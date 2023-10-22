from instagrapi.exceptions import ChallengeRequired, FeedbackRequired

from helpers.configutils import read_config
from helpers.logutils import clientlogger, consolelog, joblogger
from helpers.stringutils import str_to_bool

silent_mode = str_to_bool(read_config("logs", "silent", False))


def unlike_media(posts, client):
    for post in posts:
        try:
            client.media_unlike(post.id)

        except FeedbackRequired as e:
            clientlogger.error(f"Rate limited: {e}")
            return False

        except ChallengeRequired:
            clientlogger.error(f"Rate limited: Complete captcha by logging in to web")
            return False

        except Exception as e:
            clientlogger.error(f"Unexpected error: {e}")
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
    status = True

    while (status is True) and (
        liked_medias := client.liked_medias(
            int(read_config("ratelimit", "max_fetch_count", 25))
        )
    ):
        joblogger.info(
            f"Fetching {int(read_config('ratelimit', 'max_fetch_count', 25))} recently liked posts"
        )

        joblogger.debug(liked_medias)

        status = unlike_media(liked_medias, client)
