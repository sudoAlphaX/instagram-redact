from client import cl
from handlers import unlike_export, unlike_web
from helpers.configutils import read_config


def main():
    """
    The main function is the entry point for this program.
    It will run all of the tasks that are enabled in config.ini, and then exit.

    Doc Author:
        Trelent
    """

    if read_config("tasks", "unlike_web", False):
        unlike_export.unlike_all(cl)

    if read_config("tasks", "unlike_export", False):
        unlike_web.unlike_all(cl)


if __name__ == "__main__":
    main()
