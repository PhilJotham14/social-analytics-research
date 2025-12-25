from datetime import datetime, timezone
from typing import Iterable, Dict, Any


def in_week(ts: int, week_start: datetime, week_end: datetime) -> bool:
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return week_start <= dt <= week_end


def bucket_items(items: Iterable[Dict[str, Any]], week_start: datetime, week_end: datetime):
    return [it for it in items if "created_utc" in it and in_week(it["created_utc"], week_start, week_end)]
