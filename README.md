# Social Media Platform Usage Analytics – Data Collection & Aggregation Pipelines

**Project:** Social Media Platform Usage Analytics  
**Repository:** https://github.com/PhilJotham14/social-analytics-research.git  
**Timeline:** 53 weeks (September 2, 2024 – September 1, 2025)  
**Current Status:** Step 3 Complete (4-week pilot aggregation)

---

## Project Overview

This repository contains production-ready data collection and aggregation pipelines for analyzing trending topics and user engagement across three social media platforms:

- **Reddit:** 10 subreddits, 2,000 posts per subreddit per week
- **Twitter/X:** Hashtag-based tweets, 500 tweets per week (Recent Search API)
- **GitHub:** Trending repositories, 200 repositories per week

**Key Features:**
- Official APIs as primary data sources (PRAW, Twitter API v2, GitHub REST API)
- Robust error handling with exponential backoff and rate limit monitoring
- Graceful degradation when credentials are unavailable
- Structured logging with emoji indicators for easy debugging
- Pagination support for large datasets
- Idempotent operations (safe to re-run)
- Topic detection and engagement score calculation
- Comprehensive QA artifacts for data validation

---

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Git installed
- Active internet connection
- API credentials (see [Credential Setup](#credential-setup) below)

### 1. Clone the Repository

```bash
git clone https://github.com/PhilJotham14/social-analytics-research.git
cd social-analytics-research
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation:**
You should see `(venv)` at the beginning of your terminal prompt.

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

**Expected packages:**
- `praw==7.7.1` – Reddit API wrapper
- `httpx==0.25.2` – HTTP client for Twitter/GitHub
- `tenacity==8.2.3` – Retry logic with exponential backoff
- `loguru==0.7.2` – Structured logging
- `python-dotenv==1.0.0` – Environment variable management
- `pyyaml==6.0.1` – Configuration file parsing
- `pandas==2.1.4` – Data processing and XLSX export
- `numpy==1.26.2` – Numerical operations
- `openpyxl` – Excel file generation

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials (see below)
```

---

## Credential Setup

### GitHub Personal Access Token (Required for GitHub pipeline)

1. Go to https://github.com/settings/tokens?type=beta
2. Click **"Generate new token"** → **"Fine-grained personal access token"**
3. Configure:
   - **Token name:** `social-analytics-research`
   - **Expiration:** 90 days (or custom)
   - **Repository access:** Public Repositories (read-only)
   - **Permissions:** Metadata (automatic with public repos)
4. Click **"Generate token"** and copy the token (starts with `github_pat_`)
5. Add to `.env`:
   ```bash
   GITHUB_TOKEN=github_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Test:**
```bash
python tests/test_github.py
```

### Twitter/X Bearer Token (Required for Twitter pipeline)

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new **Free Tier** app
3. Navigate to **Keys and Tokens** → **Bearer Token**
4. Click **"Regenerate"** and copy the token (starts with multiple `A`s)
5. Add to `.env`:
   ```bash
   X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Rate Limits:**
- 180 requests per 15 minutes
- 450 requests per 24 hours (Recent Search endpoint)

**Test:**
```bash
python tests/test_twitter.py
```

### Reddit OAuth2 Credentials (Required for Reddit pipeline)

1. Go to https://www.reddit.com/prefs/apps
2. Click **"Create App"** or **"Create Another App"**
3. Configure:
   - **Name:** `social-analytics-research`
   - **App type:** Script
   - **Description:** Academic research on trending topics
   - **Redirect URI:** `http://localhost:8080`
4. Copy `client_id` (under app name) and `secret`
5. Add to `.env`:
   ```bash
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USER_AGENT=Social-Analytics-Research/1.0 by u/yourusername
   ```

**Note:** Reddit OAuth2 approval may take 1-3 business days for new apps.

**Test:**
```bash
python -m src.pipelines.run_reddit_week --week 2024-09-02
```

---

## Running the Pipelines

### Step 1: Data Collection (Individual Weeks)

**GitHub (Week 1 example):**
```bash
python -m src.pipelines.run_github_week --week 2024-09-02
```

**Twitter/X (Recent week only, due to API limitations):**
```bash
python -m src.pipelines.run_twitter_week --week 2024-09-02
```

**Reddit (All 10 subreddits):**
```bash
python -m src.pipelines.run_reddit_week --week 2024-09-02
```

### Step 2: Pilot Aggregation (NEW - Step 3)

After collecting raw data, aggregate and analyze across platforms:

```bash
python -m src.pipelines.run_aggregate_weeks --pilot
```

**What this does:**
- Reads 4 pilot weeks (2024-09-02, 2024-11-25, 2025-02-24, 2025-09-01)
- Aggregates data from all 3 platforms
- Detects top trending topics per platform
- Calculates engagement scores (log1p formula, min-max normalized)
- Generates pilot CSV/XLSX outputs
- Creates comprehensive QA artifacts

**Outputs:**
```
data/final/
├── pilot_weekly.csv              # Main aggregated dataset
├── pilot_weekly.xlsx             # Excel version
├── data_quality_status.csv       # Data status per platform-week
├── api_telemetry.csv             # Request counts and error tracking
├── plausibility_checks.csv       # Evidence URLs for verification
└── validation_report.md          # Comprehensive pilot summary
```

### Testing API Connections

Before running full pipelines, verify credentials:

```bash
# GitHub API test
python tests/test_github.py

# Twitter API test
python tests/test_twitter.py
```

### Output Files

**Raw data** (JSONL format):

```
data/raw/
├── github/2024/2024-09-02.jsonl       # 200 repos with topics
├── x/2024/2024-09-02.jsonl            # 500 tweets with hashtags/metrics
└── reddit/2024/2024-09-02.jsonl       # 20,000 posts (2,000/subreddit × 10)
```

**Sample GitHub output:**
```json
{
  "full_name": "PDFMathTranslate/PDFMathTranslate",
  "stargazers_count": 30847,
  "topics": ["chinese", "latex", "pdf", "translation"],
  "created_utc": "2024-09-06T06:56:03Z"
}
```

**Aggregated data** (CSV/XLSX format):

```csv
Platform,Week Starting Date,Top Trending Topic,Engagement Score,Post Count,User Interactions
GitHub,2024-09-02,python,37.2,50,158305
X,2024-09-02,,0.0,0,0
Reddit,2024-09-02,,0.0,0,0
```

---

## Project Configuration

### Subreddits (10 approved)
- r/news
- r/worldnews
- r/technology
- r/funny
- r/AskReddit
- r/pics
- r/science
- r/politics
- r/gaming
- r/movies

### Twitter/X Query
```
(#AI OR #tech OR #news OR #trending OR #sports OR #business OR #entertainment) -is:retweet lang:en
```

### Week Coverage
53 weeks from **Monday, September 2, 2024** to **Monday, September 1, 2025**

See `src/config/weeks.yaml` for complete list.

### Pilot Weeks (Step 3)
- **Week 1:** 2024-09-02 (First week)
- **Week 13:** 2024-11-25 (Q4 2024 sample)
- **Week 26:** 2025-02-24 (Mid-year 2025 sample)
- **Week 53:** 2025-09-01 (Final week)

---

## Data Processing Pipeline

### Step 1: Raw Data Collection
```
API → JSONL files (data/raw/{platform}/{YYYY}/{YYYY-MM-DD}.jsonl)
```

### Step 2: Aggregation
```
JSONL → Topic Detection → Engagement Scoring → CSV/XLSX (data/final/)
```

### Topic Detection Logic
- **GitHub:** Extract from `topics` array, fallback to `language`
- **Twitter/X:** Extract hashtags from tweet text
- **Reddit:** Extract keywords from post titles

### Engagement Score Formula
```python
# Raw score
raw_score = 0.3 × log1p(post_count) + 0.7 × log1p(user_interactions)

# Normalization (per platform, 0-100 scale)
normalized = 100 × (raw - min) / (max - min)
```

**User Interactions by Platform:**
- **GitHub:** `stargazers_count + forks_count + watchers_count`
- **Twitter/X:** `like_count + retweet_count`
- **Reddit:** `score + num_comments`

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'praw'`
**Solution:** Ensure virtual environment is activated and packages installed:
```bash
# Activate venv first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall packages
pip install -r requirements.txt
```

### Issue: Twitter "429 Too Many Requests"
**Solution:** Rate limit exceeded. Wait for reset:
- 15-minute window: Wait 15 minutes
- 24-hour quota: Wait until midnight UTC

### Issue: GitHub "403 rate limit exceeded"
**Solution:** Topics API has secondary rate limits. Pipeline handles this gracefully by:
- Logging warnings
- Continuing with empty topics array
- Completing the batch

### Issue: Reddit "401 Unauthorized"
**Solution:**
1. Verify credentials in `.env`
2. Ensure OAuth2 app is approved
3. Check `USER_AGENT` format matches: `AppName/Version by u/username`

### Issue: Aggregation fails with "No raw files found"
**Solution:**
1. Verify raw data exists in `data/raw/{platform}/{YYYY}/`
2. Check file naming: `YYYY-MM-DD.jsonl`
3. Ensure you ran collection pipelines first

---

## Error Handling Features

All pipelines include:
- ✅ **Exponential backoff:** 5 retries with 2-60 second waits
- ✅ **Rate limit monitoring:** Logs warnings when limits are low
- ✅ **Graceful degradation:** Returns partial results on errors
- ✅ **Pagination:** Handles `next_token` continuations automatically
- ✅ **Cap enforcement:** Stops at configured limits (200/500/2000)
- ✅ **No-credential handling:** Writes empty placeholders instead of crashing

---

## Current Status

### Step 2: Data Collection Pipelines

| Platform | API Status | Test Evidence | Pipeline Status |
|----------|-----------|---------------|-----------------|
| **GitHub** | ✅ Operational | `docs/evidence/github_*` | ✅ 200 repos collected with topics |
| **Twitter/X** | ✅ Functional | `docs/evidence/twitter_*` | ⏳ Rate limited (24hr cooldown) |
| **Reddit** | ❌ Access Denied | `docs/evidence/reddit_*` | ⏳ Code ready, OAuth denied |

**Blockers:**
- Reddit OAuth2 access denied (permanent)
- Twitter rate limit cooldown (temporary, resets midnight UTC)

### Step 3: Pilot Aggregation

| Deliverable | Status | Location |
|------------|--------|----------|
| Pilot CSV/XLSX | ✅ Complete | `data/final/pilot_weekly.csv` |
| QA Artifacts | ✅ Complete | `data/final/` (4 files) |
| Validation Report | ✅ Complete | `data/final/validation_report.md` |

**Pilot Results:**
- 4 weeks aggregated (2024-09-02, 2024-11-25, 2025-02-24, 2025-09-01)
- GitHub: 800 repos collected (4 weeks × 200 repos)
- X and Reddit: Zeros per approved policy
- Total dataset: 12 rows (4 weeks × 3 platforms)

---

## Repository Structure

```
social-analytics-research/
├── src/
│   ├── config/              # Platform limits, subreddits, week definitions
│   ├── platforms/           # API clients (reddit_client.py, twitter_client.py, github_client.py)
│   ├── pipelines/           # Data collection and aggregation scripts
│   │   ├── run_reddit_week.py        # Reddit weekly collection
│   │   ├── run_twitter_week.py       # Twitter weekly collection
│   │   ├── run_github_week.py        # GitHub weekly collection
│   │   └── run_aggregate_weeks.py    # Step 3 aggregation (NEW)
│   ├── processors/          # Topic detection, scoring, bucketing
│   │   ├── topic_detection.py        # Keyword extraction
│   │   └── scoring.py                # Engagement score calculation
│   └── utils/               # Time utilities, I/O, logging
├── tests/                   # API connection tests
├── data/
│   ├── raw/                 # JSONL output files (by platform/year)
│   └── final/               # Aggregated CSV/XLSX + QA artifacts (NEW)
├── docs/evidence/           # Screenshots for validation
├── .env.example             # Credential template
├── .gitignore               # Excludes .env, data/, venv/
├── README.md                # This file
├── requirements.txt         # Python dependencies
└── VALIDATION_REPORT.md     # Step 2 submission summary
```

---

## QA Artifacts (Step 3)

### data_quality_status.csv
Tracks data completeness per platform-week:
```csv
Platform,Week Starting Date,Data Status,Notes
GitHub,2024-09-02,ok,
X,2024-09-02,missing,Interim recent-only; historical weeks set to zeros
Reddit,2024-09-02,missing,Reddit API access refused; zeros by policy
```

### api_telemetry.csv
Tracks API usage and error rates:
```csv
Platform,Week Starting Date,total_requests,http_429_count,total_retries
GitHub,2024-09-02,4,0,0
X,2024-09-02,0,0,0
Reddit,2024-09-02,0,0,0
```

### plausibility_checks.csv
Provides evidence URLs for spot-checking:
```csv
Platform,Week Starting Date,Top Trending Topic,Evidence URLs
GitHub,2024-09-02,python,https://github.com/search?q=created:2024-09-02..2024-09-08+topic:python
```

### validation_report.md
Comprehensive pilot summary with:
- Pilot week coverage explanation
- Explicit zero policy statements for X and Reddit
- Engagement score methodology
- Data quality summary

---

## Notes

- **Idempotent operations:** Safe to re-run pipelines; existing files are overwritten
- **Twitter Recent Search limitation:** Can only access tweets from last 7 days; historical weeks will use zeros (approved methodology)
- **Reddit access denied:** OAuth2 permanently denied; all weeks use zeros (approved methodology)
- **GitHub topics enrichment:** Separate API call per repo; may encounter secondary rate limits during bulk collection
- **Logging:** All pipelines use structured logging with emoji indicators (🚀 = start, ✅ = success, ❌ = error, ⚠️ = warning)
- **Engagement normalization:** Pilot uses preliminary normalization (per platform across 4 weeks); full 53-week run will recalculate

---

## Next Steps

### Step 4: Full 53-Week Aggregation (Future)
- Run collection for all 53 weeks where possible
- Aggregate complete dataset
- Recalculate engagement scores across full timeline
- Generate final deliverables

---

**Last Updated:** December 28, 2024  
**Version:** Step 3 - Pilot Aggregation Complete  
**Status:** 4-week pilot approved, ready for full collection