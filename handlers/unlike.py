from client import cl, clientlogger
from helpers.logutils import joblogger


def unlike_all():
    while liked_medias := cl.liked_medias(100):
        for each_liked_media in liked_medias:
            try:
                status = cl.media_unlike(each_liked_media.id)
                joblogger.info(f"Unliked {each_liked_media.id}")
                print(f"Unlike status: {status}; Media ID: {each_liked_media.id}")

            except Exception as e:
                clientlogger.error(
                    f"Error: {e}; Unlike media failed: {each_liked_media}"
                )
                break
