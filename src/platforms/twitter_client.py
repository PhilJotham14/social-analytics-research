import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import httpx
from src.utils.io import write_jsonl

BASE_URL = "https://api.twitter.com/2/tweets/search/recent"


class TwitterClient:
    def __init__(self):
        self.bearer = os.getenv("X_BEARER_TOKEN")

    def _headers(self):
        return {"Authorization": f"Bearer {self.bearer}"}

    def fetch_hashtag_tweets(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        # Skeleton: recent-only; real pagination and params to be added in Step 3
        if not self.bearer:
            return []
        params = {
            "query": "has:hashtags -is:retweet",
            "start_time": start.isoformat().replace("+00:00", "Z"),
            "end_time": end.isoformat().replace("+00:00", "Z"),
            "tweet.fields": "created_at,public_metrics,entities",
            "max_results": 10,
        }
        try:
            r = httpx.get(BASE_URL, params=params, headers=self._headers(), timeout=30)
            r.raise_for_status()
            data = r.json().get("data", [])
            items: List[Dict[str, Any]] = []
            for t in data:
                created = t.get("created_at")
                items.append({
                    "id": t.get("id"),
                    "created_utc": int(datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp()) if created else None,
                    "public_metrics": t.get("public_metrics", {}),
                    "hashtags": [h.get("tag") for h in (t.get("entities", {}).get("hashtags") or [])],
                })
            return items
        except Exception:
            return []

    @staticmethod
    def write_raw(path: Path, items: List[Dict[str, Any]]):
        write_jsonl(path, items)
