import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

try:
    import praw
except Exception:  # pragma: no cover
    praw = None

from src.utils.io import write_jsonl


class RedditClient:
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "SocialAnalytics/1.0")
        if praw and self.client_id and self.client_secret:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
            )
        else:
            self.reddit = None

    def fetch_submissions(self, subreddit: str, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        if not self.reddit:
            return results
        try:
            sub = self.reddit.subreddit(subreddit)
            for s in sub.new(limit=None):
                created = getattr(s, "created_utc", None)
                if created is None:
                    continue
                if created < start.timestamp():
                    break
                if start.timestamp() <= created <= end.timestamp():
                    results.append({
                        "id": s.id,
                        "title": s.title,
                        "score": s.score,
                        "num_comments": s.num_comments,
                        "created_utc": int(created),
                        "subreddit": subreddit,
                    })
        except Exception:
            pass
        return results

    @staticmethod
    def write_raw(path: Path, items: List[Dict[str, Any]]):
        write_jsonl(path, items)
