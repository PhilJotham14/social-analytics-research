"""Test GitHub API connection"""

# how to run the file with the command - python tests/test_github.py

import os
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    print("❌ ERROR: GITHUB_TOKEN not found in .env file!")
    print("Please add your GitHub token to the .env file")
    exit(1)

# Test GitHub API
print("Testing GitHub API connection...")
print(f"Token starts with: {token[:10]}...")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

try:
    # Search for repos created in first week
    r = httpx.get(
        "https://api.github.com/search/repositories",
        params={
            "q": "created:2024-09-02..2024-09-08",
            "sort": "stars",
            "order": "desc",
            "per_page": 5,
        },
        headers=headers,
        timeout=10,
    )

    if r.status_code == 200:
        data = r.json()
        total = data.get("total_count", 0)
        items = data.get("items", [])

        print("✅ SUCCESS! GitHub token works!")
        print(f"📊 Found {total} total repos created in Week 1")
        print(f"📦 Retrieved {len(items)} sample repos")

        if items:
            print("\n🌟 Top repos from Week 1:")
            for i, repo in enumerate(items, 1):
                print(
                    f'  {i}. {repo["full_name"]} - ⭐ {repo["stargazers_count"]} stars'
                )

        # Check rate limit
        remaining = r.headers.get("x-ratelimit-remaining")
        print(f"\n📈 Rate limit remaining: {remaining} requests")

    elif r.status_code == 401:
        print("❌ AUTHENTICATION FAILED!")
        print("Your GitHub token is invalid or expired.")
        print("Please generate a new token at: https://github.com/settings/tokens")

    elif r.status_code == 403:
        print("❌ RATE LIMIT EXCEEDED or PERMISSION DENIED")
        print("Wait a moment and try again, or check token permissions.")

    else:
        print(f"❌ ERROR: HTTP {r.status_code}")
        print(f"Response: {r.text}")

except Exception as e:
    print(f"❌ CONNECTION ERROR: {e}")
    print("Check your internet connection and try again.")
