from datetime import datetime, timedelta, timezone

import humanize


def relative_time(label: str, dt: datetime):
    humanize.i18n.activate("pt_BR")  # type: ignore

    if not dt:
        return {
            "body": f"**{label}:** N/A",
        }

    now = datetime.now(timezone.utc)
    diff = now - dt

    return {
        "body": f"**{label}:** {humanize.naturaltime(diff)}",
        "help": dt.astimezone(timezone(timedelta(hours=-3))).strftime(
            "%Y-%m-%d %H:%M:%S UTC-3"
        ),
    }
