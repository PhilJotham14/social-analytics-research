"""Test Twitter/X API connection"""

# Run Twitter test
# python tests/test_twitter.py

import os
from dotenv import load_dotenv
import httpx
from datetime import datetime, timedelta, timezone

# Load environment variables
load_dotenv()
token = os.getenv("X_BEARER_TOKEN")

if not token:
    print("❌ ERROR: X_BEARER_TOKEN not found in .env file!")
    exit(1)

print("Testing Twitter/X API connection...")
print(f"Token starts with: {token[:20]}...")

headers = {
    "Authorization": f"Bearer {token}",
}

# Test with a recent search (last 7 days)
# IMPORTANT: Twitter requires end_time to be at least 10 seconds in the past
end_time = datetime.now(timezone.utc) - timedelta(
    seconds=30
)  # 30 seconds ago for safety
start_time = end_time - timedelta(days=1)  # Search last 24 hours

print(
    f"Searching tweets from {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC"
)

# FIXED: Added actual search terms with the operators
# Twitter requires at least one keyword/hashtag along with operators
params = {
    "query": "(#AI OR #tech OR #news OR #trending OR #sports) -is:retweet lang:en",  # FIXED
    "start_time": start_time.isoformat().replace("+00:00", "Z"),
    "end_time": end_time.isoformat().replace("+00:00", "Z"),
    "tweet.fields": "created_at,public_metrics,entities",
    "max_results": 10,
}

print(f"Query: {params['query']}")  # Show the query being used

try:
    r = httpx.get(
        "https://api.twitter.com/2/tweets/search/recent",
        params=params,
        headers=headers,
        timeout=10,
    )

    if r.status_code == 200:
        data = r.json()
        tweets = data.get("data", [])
        meta = data.get("meta", {})

        print("✅ SUCCESS! Twitter token works!")
        print(f'📊 Result count: {meta.get("result_count", 0)}')
        print(f"📦 Retrieved {len(tweets)} sample tweets")

        if tweets:
            print("\n🐦 Sample tweets:")
            for i, tweet in enumerate(tweets[:5], 1):
                metrics = tweet.get("public_metrics", {})
                hashtags = [
                    h.get("tag") for h in tweet.get("entities", {}).get("hashtags", [])
                ]
                print(
                    f'  {i}. Likes: {metrics.get("like_count", 0)} | '
                    f'Retweets: {metrics.get("retweet_count", 0)} | '
                    f'Hashtags: {", ".join(hashtags[:3]) if hashtags else "none"}'
                )

        # Check rate limit
        remaining = r.headers.get("x-rate-limit-remaining")
        limit = r.headers.get("x-rate-limit-limit")
        print(f"\n📈 Rate limit: {remaining}/{limit} requests remaining")

    elif r.status_code == 401:
        print("❌ AUTHENTICATION FAILED!")
        print("Your Twitter Bearer Token is invalid or expired.")

    elif r.status_code == 429:
        print("❌ RATE LIMIT EXCEEDED")
        print("Wait 15 minutes and try again.")

    elif r.status_code == 400:
        print("❌ BAD REQUEST!")
        print(f"Response: {r.text}")
        print("\nCommon issues:")
        print("- Query syntax error (need at least one keyword with operators)")
        print("- end_time must be at least 10 seconds in the past")

    else:
        print(f"❌ ERROR: HTTP {r.status_code}")
        print(f"Response: {r.text}")

except Exception as e:
    print(f"❌ CONNECTION ERROR: {e}")
    import traceback

    traceback.print_exc()
