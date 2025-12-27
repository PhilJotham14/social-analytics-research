# import os
# from pathlib import Path
# from typing import List, Dict, Any
# from datetime import datetime
# import httpx
# from src.utils.io import write_jsonl

# BASE_URL = "https://api.twitter.com/2/tweets/search/recent"


# class TwitterClient:
#     def __init__(self):
#         self.bearer = os.getenv("X_BEARER_TOKEN")

#     def _headers(self):
#         return {"Authorization": f"Bearer {self.bearer}"}

#     def fetch_hashtag_tweets(
#         self, start: datetime, end: datetime
#     ) -> List[Dict[str, Any]]:
#         # Skeleton: recent-only; real pagination and params to be added in Step 3
#         if not self.bearer:
#             return []
#         params = {
#             "query": "has:hashtags -is:retweet",
#             "start_time": start.isoformat().replace("+00:00", "Z"),
#             "end_time": end.isoformat().replace("+00:00", "Z"),
#             "tweet.fields": "created_at,public_metrics,entities",
#             "max_results": 10,
#         }
#         try:
#             r = httpx.get(BASE_URL, params=params, headers=self._headers(), timeout=30)
#             r.raise_for_status()
#             data = r.json().get("data", [])
#             items: List[Dict[str, Any]] = []
#             for t in data:
#                 created = t.get("created_at")
#                 items.append(
#                     {
#                         "id": t.get("id"),
#                         "created_utc": (
#                             int(
#                                 datetime.fromisoformat(
#                                     created.replace("Z", "+00:00")
#                                 ).timestamp()
#                             )
#                             if created
#                             else None
#                         ),
#                         "public_metrics": t.get("public_metrics", {}),
#                         "hashtags": [
#                             h.get("tag")
#                             for h in (t.get("entities", {}).get("hashtags") or [])
#                         ],
#                     }
#                 )
#             return items
#         except Exception:
#             return []

#     @staticmethod
#     def write_raw(path: Path, items: List[Dict[str, Any]]):
#         write_jsonl(path, items)

# complete fixed version with pagination loop.
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from loguru import logger
from src.utils.io import write_jsonl

BASE_URL = "https://api.twitter.com/2/tweets/search/recent"


class TwitterClient:
    def __init__(self):
        self.bearer = os.getenv("X_BEARER_TOKEN")
        self.max_results_per_request = 100  # Twitter API max

    def _headers(self):
        """Generate request headers with Bearer token"""
        return {"Authorization": f"Bearer {self.bearer}"}

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TimeoutException)),
        reraise=True,
    )
    def _make_request(self, params: dict):
        """Make rate-limited request with exponential backoff"""
        r = httpx.get(BASE_URL, params=params, headers=self._headers(), timeout=30)

        # Log rate limit status
        remaining = r.headers.get("x-rate-limit-remaining")
        if remaining and int(remaining) < 5:
            logger.warning(f"⚠️  Twitter rate limit low: {remaining} requests remaining")

        r.raise_for_status()
        return r.json()

    def fetch_hashtag_tweets(
        self, start: datetime, end: datetime, max_tweets: int = 500
    ) -> List[Dict[str, Any]]:
        """Fetch tweets with hashtags - WITH PAGINATION"""
        if not self.bearer:
            logger.warning("⚠️  No Twitter bearer token")
            return []

        items: List[Dict[str, Any]] = []
        next_token = None

        base_params = {
            # FIXED: Added actual search terms with operators (already done!)
            "query": "(#AI OR #tech OR #news OR #trending OR #sports OR #business OR #entertainment) -is:retweet lang:en",
            "start_time": start.isoformat().replace("+00:00", "Z"),
            "end_time": end.isoformat().replace("+00:00", "Z"),
            "tweet.fields": "created_at,public_metrics,entities",
            "max_results": min(self.max_results_per_request, max_tweets),
        }

        logger.info(f"📥 Fetching Twitter tweets (max={max_tweets})")
        logger.debug(
            f"Query: {base_params['query']}"
        )  # ADD THIS LINE (only change needed!)

        try:
            page = 1
            while len(items) < max_tweets:
                params = base_params.copy()
                if next_token:
                    params["next_token"] = next_token

                logger.debug(f"Twitter page {page} (collected: {len(items)})")
                data = self._make_request(params)

                tweets = data.get("data", [])
                if not tweets:
                    logger.info("No more tweets available")
                    break

                for t in tweets:
                    created = t.get("created_at")
                    items.append(
                        {
                            "id": t.get("id"),
                            "created_utc": (
                                int(
                                    datetime.fromisoformat(
                                        created.replace("Z", "+00:00")
                                    ).timestamp()
                                )
                                if created
                                else None
                            ),
                            "public_metrics": t.get("public_metrics", {}),
                            "hashtags": [
                                h.get("tag")
                                for h in (t.get("entities", {}).get("hashtags") or [])
                            ],
                        }
                    )

                next_token = data.get("meta", {}).get("next_token")
                if not next_token:
                    break

                if len(items) >= max_tweets:
                    logger.info(f"🛑 Reached cap of {max_tweets}")
                    break

                page += 1

            logger.info(f"✅ Twitter: Collected {len(items)} tweets")
            return items[:max_tweets]

        except Exception as e:
            logger.error(f"❌ Twitter error: {e}")
            return items

    @staticmethod
    def write_raw(path: Path, items: List[Dict[str, Any]]):
        path.parent.mkdir(parents=True, exist_ok=True)
        write_jsonl(path, items)
