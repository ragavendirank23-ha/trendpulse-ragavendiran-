# ---------------------------------------------
# TrendPulse - Task 2: Data Cleaning
# ---------------------------------------------
# This script:
# 1. Loads the latest JSON file from data/
# 2. Cleans duplicates, missing values, and low-quality data
# 3. Fixes data types and whitespace issues
# 4. Saves cleaned data as CSV
# ---------------------------------------------

import pandas as pd
import os
import glob


def get_latest_file():
    """Find the latest JSON file in data folder"""
    files = glob.glob("data/trends_*.json")
    if not files:
        return None
    return max(files, key=os.path.getctime)


def main():

    # Step 1: Load JSON file
    file_path = get_latest_file()

    if file_path is None:
        print("No JSON file found in data folder")
        return

    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}")

    # Step 2: Remove duplicates
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # Step 3: Remove missing values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Step 4: Fix data types safely
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

    df = df.dropna(subset=["score", "num_comments"])

    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # Step 5: Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Step 6: Clean whitespace in title
    df["title"] = df["title"].astype(str).str.strip()

    # Step 7: Save cleaned CSV
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSaved {len(df)} rows to {output_path}")

    # Step 8: Print category summary (aligned format)
    print("\nStories per category:")
    category_counts = df["category"].value_counts()

    for category, count in category_counts.items():
        print(f"{category:<15} {count}")


# Run the script
if __name__ == "__main__":
    main()