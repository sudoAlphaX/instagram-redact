import json
import os
import pickle


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


def dump_variable(var, file="temp/remaining_posts.dump"):
    if subdirectory := os.path.dirname(file):
        clientlogger.debug("'temp' directory absent. Attempt to create directory")
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

            dump_variable(liked_medias := format_export())

            clientlogger.info(
                "Processed 'liked_posts.json' export file. Renaming to 'old_liked_posts.json'"
            )

            return liked_medias

        else:
            clientlogger.warn(
                "'liked_posts.json' not found in export directory. Paste the .json file. Read README for more help."
            )

            return None


pending_liked_medias = get_liked_medias()

