import argparse
from pathlib import Path
from datetime import datetime, timezone
from src.platforms.github_client import GitHubClient


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True, help="Week starting date YYYY-MM-DD (Monday)")
    args = ap.parseArgs() if hasattr(ap, 'parseArgs') else ap.parse_args()
    week = args.week
    start = datetime.fromisoformat(week).replace(tzinfo=timezone.utc)
    end = start.replace()  # not used; we use created range by dates
    start_s = week
    end_s = (start + timedelta(days=6)).strftime("%Y-%m-%d")

    client = GitHubClient()
    items = client.search_repos_for_week(start_s, end_s, per_page=50)
    out = Path(f"data/raw/github/{start.year}/{week}.jsonl")
    client.write_raw(out, items)


if __name__ == "__main__":
    main()
