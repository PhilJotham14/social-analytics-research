# Social Media Platform Usage Analytics – Data Collection Pipelines

**Project:** Social Media Platform Usage Analytics (Step 2)  
**Repository:** https://github.com/PhilJotham14/social-analytics-research.git  
**Timeline:** 53 weeks (September 2, 2024 – September 1, 2025)

---

## Project Overview

This repository contains production-ready data collection pipelines for analyzing trending topics and user engagement across three social media platforms:

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

---

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Git installed
- Active internet connection
- API credentials (see [Credential Setup](#-credential-setup) below)

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
- `pandas==2.1.4` – Data processing
- `numpy==1.26.2` – Numerical operations

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

### Individual Platform Pipelines

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

### Testing API Connections

Before running full pipelines, verify credentials:

```bash
# GitHub API test
python tests/test_github.py

# Twitter API test
python tests/test_twitter.py
```

### Output Files

All raw data is stored in JSONL format:

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

---

## 🔧 Error Handling Features

All pipelines include:
- ✅ **Exponential backoff:** 5 retries with 2-60 second waits
- ✅ **Rate limit monitoring:** Logs warnings when limits are low
- ✅ **Graceful degradation:** Returns partial results on errors
- ✅ **Pagination:** Handles `next_token` continuations automatically
- ✅ **Cap enforcement:** Stops at configured limits (200/500/2000)
- ✅ **No-credential handling:** Writes empty placeholders instead of crashing

---

## 📈 Current Status

| Platform | API Status | Test Evidence | Pipeline Status |
|----------|-----------|---------------|-----------------|
| **GitHub** | ✅ Operational | `docs/evidence/github_*` | ✅ 200 repos collected with topics |
| **Twitter/X** | ✅ Functional | `docs/evidence/twitter_*` | ⏳ Rate limited (24hr cooldown) |
| **Reddit** | ⏳ Pending OAuth2 | `docs/evidence/reddit_*` | ⏳ Code ready, awaiting approval |

**Blockers:**
- Reddit OAuth2 approval pending (submitted Dec 25, 2024, ETA 1-3 business days)
- Twitter rate limit cooldown (temporary, resets midnight UTC)

---

## Repository Structure

```
social-analytics-research/
├── src/
│   ├── config/              # Platform limits, subreddits, week definitions
│   ├── platforms/           # API clients (reddit_client.py, twitter_client.py, github_client.py)
│   ├── pipelines/           # Weekly data collection scripts
│   ├── processors/          # Topic detection, scoring, bucketing
│   └── utils/               # Time utilities, I/O, logging
├── tests/                   # API connection tests
├── data/raw/                # JSONL output files
├── docs/evidence/           # Screenshots for validation
├── .env.example             # Credential template
├── .gitignore               # Excludes .env, data/, venv/
├── README.md                # This file
├── requirements.txt         # Python dependencies
└── VALIDATION_REPORT.md     # Step 2 submission summary
```

---

## Notes

- **Idempotent operations:** Safe to re-run pipelines; existing files are overwritten
- **Twitter Recent Search limitation:** Can only access tweets from last 7 days; historical weeks will use zeros (approved methodology)
- **GitHub topics enrichment:** Separate API call per repo; may encounter secondary rate limits during bulk collection
- **Logging:** All pipelines use structured logging with emoji indicators (🚀 = start, ✅ = success, ❌ = error, ⚠️ = warning)

---

**Last Updated:** December 27, 2024  
**Version:** Step 2 - Data Collection Pipelines