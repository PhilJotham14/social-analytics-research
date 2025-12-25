import argparse
from pathlib import Path
from datetime import datetime, timezone
import yaml
from src.platforms.reddit_client import RedditClient
from src.utils.time_utils import week_bounds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True, help="Week starting date YYYY-MM-DD (Monday)")
    args = ap.parse_args()
    week = args.week
    start, end = week_bounds(week)

    subs = yaml.safe_load(open("src/config/subreddits.yaml"))['subreddits']
    client = RedditClient()
    items = []
    for s in subs:
        items.extend(client.fetch_submissions(s, start, end))
    out = Path(f"data/raw/reddit/{start.year}/{week}.jsonl")
    client.write_raw(out, items)


if __name__ == "__main__":
    main()
