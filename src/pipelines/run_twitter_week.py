# import argparse
# from pathlib import Path
# from src.platforms.twitter_client import TwitterClient
# from src.utils.time_utils import week_bounds


# def main():
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--week", required=True, help="Week starting date YYYY-MM-DD (Monday)")
#     args = ap.parse_args()
#     start, end = week_bounds(args.week)

#     client = TwitterClient()
#     items = client.fetch_hashtag_tweets(start, end)
#     out = Path(f"data/raw/x/{start.year}/{args.week}.jsonl")
#     client.write_raw(out, items)


# if __name__ == "__main__":
#     main()

import argparse
from pathlib import Path
import yaml
from loguru import logger
from dotenv import load_dotenv  # ADD THIS
from src.platforms.twitter_client import TwitterClient
from src.utils.time_utils import week_bounds

# Load environment variables
load_dotenv()  # ADD THIS


def main():
    ap = argparse.ArgumentParser(description="Fetch Twitter/X tweets for a week")
    ap.add_argument(
        "--week", required=True, help="Week starting date YYYY-MM-DD (Monday)"
    )
    args = ap.parse_args()

    week = args.week
    start, end = week_bounds(week)

    # Load config for caps
    try:
        config = yaml.safe_load(open("src/config/config.yaml"))
        max_tweets = (
            config.get("limits", {}).get("twitter", {}).get("max_tweets_per_week", 500)
        )
    except Exception:
        max_tweets = 500
        logger.warning("Could not load config; using default cap of 500")

    logger.info(
        f"🚀 Twitter week {week} ({start.date()} to {end.date()}, max {max_tweets} tweets)"
    )

    client = TwitterClient()
    items = client.fetch_hashtag_tweets(start, end, max_tweets=max_tweets)

    out = Path(f"data/raw/x/{start.year}/{week}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    client.write_raw(out, items)

    logger.info(f"💾 Wrote {len(items)} tweets to {out}")
    print(f"✅ Twitter week {week}: {len(items)} tweets collected")


if __name__ == "__main__":
    main()
