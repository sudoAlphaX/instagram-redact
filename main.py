import datetime
import time

from client import cl
from handlers import unlike_export, unlike_web
from helpers.configutils import read_config, read_section
from helpers.logutils import clientlogger, consolelog
from helpers.stringutils import str_to_bool


def main():
    status = {}

    for key in (tasks := read_section("tasks")).keys():
        status[key] = {
            "completed": False,
            "can_continue": str_to_bool(tasks.get(key, False)),
            "rate_limited": False,
            "score": 0,
        }

    while any(
        ((not value["completed"]) and value["can_continue"])
        for value in status.values()
    ):
        clientlogger.debug("Current tasks: %s", status)

        if (not (status.get("unlike_export", {}).get("completed", True))) and (
            (status.get("unlike_export", {}).get("can_continue", False))
        ):
            clientlogger.debug("Running unlike_export")
            status["unlike_export"] = unlike_export.unlike_all(
                cl, status["unlike_export"]["score"]
            )

        if (not (status.get("unlike_web", {}).get("completed", True))) and (
            (status.get("unlike_web", {}).get("can_continue", False))
        ):
            clientlogger.debug("Running unlike_web")
            status["unlike_web"] = unlike_web.unlike_all(
                cl, status["unlike_web"]["score"]
            )

        for key in [
            k for k, v in status.items() if v["completed"] or not v["can_continue"]
        ]:
            clientlogger.debug("Removed %s from pending tasks", key)
            status.pop(key)

        if len(status) == 0:
            return

        minimum_score = min(value["score"] for value in status.values())

        delay = (
            (
                (int(read_config("ratelimit", "base_delay", 60)) * 60)  # type: ignore
                * pow(
                    float(read_config("ratelimit", "multiplier", 2)),  # type: ignore
                    float(minimum_score / 100),
                )  # type: ignore
            )
            if minimum_score > 0
            else 0
        )

        clientlogger.info(
            "Pausing code execution for %s secs. Resuming at %s",
            delay,
            resume := datetime.datetime.now() + datetime.timedelta(minutes=delay),
        )

        consolelog(
            (f"Pausing code execution for {delay/60} minutes. Resuming at {resume}")
        )

        time.sleep(delay)

        for key in status:
            status[key]["score"] -= minimum_score
            if status[key]["score"] < 0:
                status[key]["score"] = 0


if __name__ == "__main__":
    main()
