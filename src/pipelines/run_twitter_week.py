import argparse
from pathlib import Path
from src.platforms.twitter_client import TwitterClient
from src.utils.time_utils import week_bounds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True, help="Week starting date YYYY-MM-DD (Monday)")
    args = ap.parse_args()
    start, end = week_bounds(args.week)

    client = TwitterClient()
    items = client.fetch_hashtag_tweets(start, end)
    out = Path(f"data/raw/x/{start.year}/{args.week}.jsonl")
    client.write_raw(out, items)


if __name__ == "__main__":
    main()
