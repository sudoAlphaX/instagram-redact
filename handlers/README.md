# Information about using the Instagram export file in [instagram-redact](https://github.com/sudoAlphaX/instagram-redact)

[instagram-redact](https://github.com/sudoAlphaX/instagram-redact) provides a way to use the Instagram export to fetch the list of liked posts instead of querying the server.

## Why to use the export file instead of directly fetching the liked posts (_unlike_web_)?

Sometimes, Instagram can rate limit your account and it will prevent the program to fetch the liked posts from the servers. In such circumstances, you can use the export file instead.

## How to obtain Instagram export file

1. Visit Instagram's "Download your information" page: <https://accountscenter.instagram.com/info_and_permissions/dyi/>

2. Click "Request a download" and select your Instagram account.

3. Click "Select types of information" and select "Likes" from the list and click "Next".

4. In the "Date range" section, select "All time" and click "Save".

5. In the "Format" section, select "JSON" and click "Save".

6. Click "Submit request".

7. In about 4 days, download the Instagram export .zip file sent to your registered email address from Instagram.

## How to use the export file in [instagram-redact](https://github.com/sudoAlphaX/instagram-redact)

1. Download the export file by following the steps [above](#how-to-obtain-instagram-export-file).

2. Extract the export file and in the "likes" folder, copy "liked_posts.json".

3. In the [instagram-redact](https://github.com/sudoAlphaX/instagram-redact) directory, create a folder names "export" and paste the export file.

4. In "config.ini", under "Tasks" section, set "unlike_export" to True and "unlike_web" to False.

5. Run [main.py](https://github.com/sudoalphax/instagram-redact/blob/main/main.py)
