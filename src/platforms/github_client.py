# import os
# from pathlib import Path
# from typing import List, Dict, Any
# import httpx
# from src.utils.io import write_jsonl

# GITHUB_API = "https://api.github.com"


# class GitHubClient:
#     def __init__(self):
#         self.token = os.getenv("GITHUB_TOKEN")

#     def _headers(self):
#         h = {"Accept": "application/vnd.github+json"}
#         if self.token:
#             h["Authorization"] = f"Bearer {self.token}"
#             h["X-GitHub-Api-Version"] = "2022-11-28"
#         return h

#     def search_repos_for_week(self, start: str, end: str, per_page: int = 50) -> List[Dict[str, Any]]:
#         # Approximate trending by stars on newly created repos within the week
#         q = f"created:{start}..{end}"
#         params = {"q": q, "sort": "stars", "order": "desc", "per_page": per_page}
#         try:
#             r = httpx.get(f"{GITHUB_API}/search/repositories", params=params, headers=self._headers(), timeout=30)
#             r.raise_for_status()
#             items: List[Dict[str, Any]] = []
#             for repo in r.json().get("items", []):
#                 items.append({
#                     "full_name": repo.get("full_name"),
#                     "stargazers_count": repo.get("stargazers_count", 0),
#                     "forks_count": repo.get("forks_count", 0),
#                     "watchers_count": repo.get("watchers_count", 0),
#                     "language": repo.get("language"),
#                     "topics": [],  # filled by topics endpoint if needed
#                     "created_utc": None,
#                 })
#             return items
#         except Exception:
#             return []

#     @staticmethod
#     def write_raw(path: Path, items: List[Dict[str, Any]]):
#         write_jsonl(path, items)

import os
from pathlib import Path
from typing import List, Dict, Any
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from loguru import logger
from src.utils.io import write_jsonl

GITHUB_API = "https://api.github.com"


class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")

    def _headers(self):
        h = {"Accept": "application/vnd.github+json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
            h["X-GitHub-Api-Version"] = "2022-11-28"
        return h

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TimeoutException)),
        reraise=True,
    )
    def _make_request(self, url: str, params: dict = None):
        r = httpx.get(url, params=params, headers=self._headers(), timeout=30)

        remaining = r.headers.get("x-ratelimit-remaining")
        if remaining and int(remaining) < 100:
            logger.warning(f"⚠️  GitHub rate limit low: {remaining}")

        r.raise_for_status()
        return r.json()

    def get_repo_topics(self, owner: str, repo: str) -> List[str]:
        """Fetch topics for a repository - THIS WAS MISSING!"""
        try:
            headers = self._headers()
            headers["Accept"] = "application/vnd.github.mercy-preview+json"

            r = httpx.get(
                f"{GITHUB_API}/repos/{owner}/{repo}/topics", headers=headers, timeout=10
            )
            r.raise_for_status()
            return r.json().get("names", [])
        except Exception as e:
            logger.debug(f"Failed to fetch topics for {owner}/{repo}: {e}")
            return []

    def search_repos_for_week(
        self, start: str, end: str, per_page: int = 50, max_repos: int = 200
    ) -> List[Dict[str, Any]]:
        """Search repos with pagination and topics enrichment"""
        items: List[Dict[str, Any]] = []
        page = 1
        q = f"created:{start}..{end}"

        logger.info(f"📥 GitHub search: {q} (max={max_repos})")

        try:
            while len(items) < max_repos:
                params = {
                    "q": q,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": per_page,
                    "page": page,
                }

                logger.debug(f"GitHub page {page} (collected: {len(items)})")
                data = self._make_request(f"{GITHUB_API}/search/repositories", params)

                repos = data.get("items", [])
                if not repos:
                    break

                for repo in repos:
                    full_name = repo.get("full_name", "")
                    if "/" not in full_name:
                        continue

                    owner, repo_name = full_name.split("/", 1)

                    # ENRICH WITH TOPICS - THIS IS THE KEY FIX!
                    topics = self.get_repo_topics(owner, repo_name)

                    items.append(
                        {
                            "full_name": full_name,
                            "stargazers_count": repo.get("stargazers_count", 0),
                            "forks_count": repo.get("forks_count", 0),
                            "watchers_count": repo.get("watchers_count", 0),
                            "language": repo.get("language"),
                            "topics": topics,  # Now populated!
                            "created_utc": repo.get("created_at"),
                        }
                    )

                    if len(items) >= max_repos:
                        break

                if page >= 10 or len(repos) < per_page:
                    break

                page += 1

            logger.info(f"✅ GitHub: Collected {len(items)} repos with topics")
            return items[:max_repos]

        except Exception as e:
            logger.error(f"❌ GitHub error: {e}")
            return items

    @staticmethod
    def write_raw(path: Path, items: List[Dict[str, Any]]):
        path.parent.mkdir(parents=True, exist_ok=True)
        write_jsonl(path, items)
