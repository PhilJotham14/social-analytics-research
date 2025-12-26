# original code with issues
# import argparse
# from pathlib import Path
# from datetime import datetime, timezone
# from src.platforms.github_client import GitHubClient
# from datetime import datetime, timedelta, timezone


# def main():
#     ap = argparse.ArgumentParser()
#     ap.add_argument(
#         "--week", required=True, help="Week starting date YYYY-MM-DD (Monday)"
#     )
#     # commented out for compatibility with some environments
#     # args = ap.parseArgs() if hasattr(ap, 'parseArgs') else ap.parse_args()
#     # Using parse_args directly for compatibility
#     args = ap.parse_args()
#     week = args.week
#     start = datetime.fromisoformat(week).replace(tzinfo=timezone.utc)
#     end = start.replace()  # not used; we use created range by dates
#     start_s = week
#     end_s = (start + timedelta(days=6)).strftime("%Y-%m-%d")

#     client = GitHubClient()
#     items = client.search_repos_for_week(start_s, end_s, per_page=50)
#     out = Path(f"data/raw/github/{start.year}/{week}.jsonl")
#     client.write_raw(out, items)


# if __name__ == "__main__":
#     main()

# complete fixed version.
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone  # ADD THIS LINE
import yaml
from loguru import logger
from src.platforms.github_client import GitHubClient


def main():
    ap = argparse.ArgumentParser(description="Fetch GitHub trending repos for a week")
    ap.add_argument(
        "--week", required=True, help="Week starting date YYYY-MM-DD (Monday)"
    )
    args = ap.parse_args()  # FIXED: was ap.parseArgs()

    week = args.week
    start = datetime.fromisoformat(week).replace(tzinfo=timezone.utc)
    end = start + timedelta(days=6)  # FIXED: compute actual end date

    start_s = week
    end_s = end.strftime("%Y-%m-%d")

    # Load config for caps
    try:
        config = yaml.safe_load(open("src/config/config.yaml"))
        max_repos = (
            config.get("limits", {}).get("github", {}).get("max_repos_per_week", 200)
        )
    except Exception:
        max_repos = 200
        logger.warning("Could not load config; using default cap of 200")

    logger.info(f"🚀 GitHub week {week} ({start_s} to {end_s}, max {max_repos} repos)")

    client = GitHubClient()
    items = client.search_repos_for_week(start_s, end_s, max_repos=max_repos)

    out = Path(f"data/raw/github/{start.year}/{week}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    client.write_raw(out, items)

    logger.info(f"💾 Wrote {len(items)} repos to {out}")
    print(f"✅ GitHub week {week}: {len(items)} repos collected with topics")


if __name__ == "__main__":
    main()
