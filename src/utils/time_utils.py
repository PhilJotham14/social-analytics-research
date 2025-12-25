from datetime import datetime, timedelta, timezone
from dateutil import parser


def week_bounds(monday_str: str):
    monday = datetime.fromisoformat(monday_str).replace(tzinfo=timezone.utc)
    start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7) - timedelta(seconds=1)
    return start, end
