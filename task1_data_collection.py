# ---------------------------------------------
# TrendPulse - Task 1: Data Collection (Final)
# ---------------------------------------------
# This version ensures:
# ✔ Category-wise loop (correct requirement)
# ✔ 2 sec delay per category
# ✔ Better keyword coverage
# ✔ Higher chance of 100+ stories
# ---------------------------------------------

import requests
import time
import json
import os
from datetime import datetime

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# Improved keywords (important fix)
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm", "startup", "programming"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global", "policy", "economy"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship", "match"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome", "experiment"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming", "video"]
}

# Check keyword match
def match_category(title, keywords):
    title = title.lower()
    return any(keyword in title for keyword in keywords)


def main():
    print("Fetching top stories...")

    # Fetch more IDs (important fix)
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        story_ids = response.json()[:1000]   # increased from 500
    except Exception as e:
        print("Error fetching top stories:", e)
        return

    collected_data = []

    # Category-wise loop (required)
    for category, keywords in categories.items():

        print(f"\nCollecting {category} stories...")
        count = 0

        for story_id in story_ids:
            if count >= 25:
                break

            try:
                response = requests.get(ITEM_URL.format(story_id), headers=headers)
                story = response.json()

                if not story or "title" not in story:
                    continue

                title = story["title"]

                # Match category
                if match_category(title, keywords):

                    data = {
                        "post_id": story.get("id"),
                        "title": title,
                        "category": category,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by", "unknown"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    collected_data.append(data)
                    count += 1

                    print(f"Added [{category}] ({count}/25)")

            except Exception as e:
                print(f"Error fetching story {story_id}: {e}")
                continue

        print(f"{category} collected: {count}")

        # Required delay (IMPORTANT)
        time.sleep(2)

    # Create data folder
    if not os.path.exists("data"):
        os.makedirs("data")

    # Save JSON
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w") as f:
        json.dump(collected_data, f, indent=4)

    # Final output
    print("\n----------------------------------")
    print(f"Collected {len(collected_data)} stories.")
    print(f"Saved to {filename}")
    print("----------------------------------")


if __name__ == "__main__":
    main()