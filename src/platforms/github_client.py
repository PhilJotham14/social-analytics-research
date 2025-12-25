import os
from pathlib import Path
from typing import List, Dict, Any
import httpx
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

    def search_repos_for_week(self, start: str, end: str, per_page: int = 50) -> List[Dict[str, Any]]:
        # Approximate trending by stars on newly created repos within the week
        q = f"created:{start}..{end}"
        params = {"q": q, "sort": "stars", "order": "desc", "per_page": per_page}
        try:
            r = httpx.get(f"{GITHUB_API}/search/repositories", params=params, headers=self._headers(), timeout=30)
            r.raise_for_status()
            items: List[Dict[str, Any]] = []
            for repo in r.json().get("items", []):
                items.append({
                    "full_name": repo.get("full_name"),
                    "stargazers_count": repo.get("stargazers_count", 0),
                    "forks_count": repo.get("forks_count", 0),
                    "watchers_count": repo.get("watchers_count", 0),
                    "language": repo.get("language"),
                    "topics": [],  # filled by topics endpoint if needed
                    "created_utc": None,
                })
            return items
        except Exception:
            return []

    @staticmethod
    def write_raw(path: Path, items: List[Dict[str, Any]]):
        write_jsonl(path, items)
