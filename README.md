# Social Media Platform Usage Analytics – Pipelines (Step 2)

This repository contains the data collection pipelines and processors for Reddit, Twitter/X, and GitHub Trending, aligned with the approved Methodology & Schema.

Highlights:
- Official APIs as primary sources (Apify not used as primary)
- Twitter/X interim: Recent Search only; historical weeks set to zeros; backfill later
- Reddit subreddits: r/news, r/worldnews, r/technology, r/funny, r/AskReddit, r/pics, r/science, r/politics, r/gaming, r/movies
- Companion QA artifacts will be produced in later steps

Setup
1. Create a virtual environment and install dependencies:
   pip install -r requirements.txt
2. Copy .env.example to .env and populate credentials.
3. Ensure weeks.yaml is present under src/config (generated in this package).

Running (pilot mode)
- Reddit week: python -m src.pipelines.run_reddit_week --week 2024-09-02
- GitHub week: python -m src.pipelines.run_github_week --week 2024-09-02
- X week (recent-only): python -m src.pipelines.run_twitter_week --week <recent Monday>
- Aggregate all: python -m src.pipelines.run_aggregate_weeks

Data paths (local default)
- data/raw/{platform}/{YYYY}/{YYYY-MM-DD}.jsonl
- data/intermediate/{platform}/{YYYY}/{YYYY-MM-DD}.parquet
- data/final/

Notes
- The code is written to be idempotent and to respect rate limits. Without credentials, the fetchers will no-op and write empty placeholders (zeros), preserving the weekly grid.
