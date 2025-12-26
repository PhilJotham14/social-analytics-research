# import os
# from pathlib import Path
# from typing import List, Dict, Any
# from datetime import datetime

# try:
#     import praw
# except Exception:  # pragma: no cover
#     praw = None

# from src.utils.io import write_jsonl


# class RedditClient:
#     def __init__(self):
#         self.client_id = os.getenv("REDDIT_CLIENT_ID")
#         self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
#         self.user_agent = os.getenv("REDDIT_USER_AGENT", "SocialAnalytics/1.0")
#         if praw and self.client_id and self.client_secret:
#             self.reddit = praw.Reddit(
#                 client_id=self.client_id,
#                 client_secret=self.client_secret,
#                 user_agent=self.user_agent,
#             )
#         else:
#             self.reddit = None

#     def fetch_submissions(self, subreddit: str, start: datetime, end: datetime) -> List[Dict[str, Any]]:
#         results: List[Dict[str, Any]] = []
#         if not self.reddit:
#             return results
#         try:
#             sub = self.reddit.subreddit(subreddit)
#             for s in sub.new(limit=None):
#                 created = getattr(s, "created_utc", None)
#                 if created is None:
#                     continue
#                 if created < start.timestamp():
#                     break
#                 if start.timestamp() <= created <= end.timestamp():
#                     results.append({
#                         "id": s.id,
#                         "title": s.title,
#                         "score": s.score,
#                         "num_comments": s.num_comments,
#                         "created_utc": int(created),
#                         "subreddit": subreddit,
#                     })
#         except Exception:
#             pass
#         return results

#     @staticmethod
#     def write_raw(path: Path, items: List[Dict[str, Any]]):
#         write_jsonl(path, items)


import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

try:
    import praw
except Exception:
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
            logger.info("✅ Reddit client initialized")
        else:
            self.reddit = None
            logger.warning("⚠️  Reddit client not initialized")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )
    def fetch_submissions(
        self,
        subreddit: str,
        start: datetime,
        end: datetime,
        max_posts: int = 2000,  # ADD THIS PARAMETER
    ) -> List[Dict[str, Any]]:
        """Fetch submissions with cap enforcement"""
        results: List[Dict[str, Any]] = []

        if not self.reddit:
            logger.warning(f"No Reddit client; skipping r/{subreddit}")
            return results

        try:
            sub = self.reddit.subreddit(subreddit)
            logger.info(f"📥 Fetching r/{subreddit} (max={max_posts})")

            for s in sub.new(limit=None):
                created = getattr(s, "created_utc", None)
                if created is None:
                    continue

                if created < start.timestamp():
                    logger.debug(f"r/{subreddit}: Reached posts before window")
                    break

                if start.timestamp() <= created <= end.timestamp():
                    results.append(
                        {
                            "id": s.id,
                            "title": s.title,
                            "score": s.score,
                            "num_comments": s.num_comments,
                            "created_utc": int(created),
                            "subreddit": subreddit,
                        }
                    )

                    # ENFORCE CAP - THIS IS THE KEY FIX!
                    if len(results) >= max_posts:
                        logger.info(f"🛑 r/{subreddit}: Reached cap of {max_posts}")
                        break

            logger.info(f"✅ r/{subreddit}: Collected {len(results)} posts")

        except Exception as e:
            logger.error(f"❌ Error fetching r/{subreddit}: {e}")

        return results

    @staticmethod
    def write_raw(path: Path, items: List[Dict[str, Any]]):
        path.parent.mkdir(parents=True, exist_ok=True)
        write_jsonl(path, items)
