# ---------------------------------------------
# TrendPulse - Task 3: Data Analysis
# ---------------------------------------------
# This script:
# 1. Loads cleaned CSV from Task 2
# 2. Performs analysis using Pandas & NumPy
# 3. Adds new columns (engagement, is_popular)
# 4. Saves analysed data to a new CSV file
# ---------------------------------------------

import pandas as pd
import numpy as np
import os


def main():

    # Step 1: Load CSV file
    file_path = "data/trends_clean.csv"

    if not os.path.exists(file_path):
        print("Error: File not found ->", file_path)
        return

    df = pd.read_csv(file_path)

    # Print shape
    print(f"Loaded data: {df.shape}")

    # Print first 5 rows
    print("\nFirst 5 rows:")
    print(df.head())

    # Average calculations
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"\nAverage score   : {avg_score:.2f}")
    print(f"Average comments: {avg_comments:.2f}")

    # -----------------------------------------
    # Step 2: NumPy Analysis
    # -----------------------------------------
    print("\n--- NumPy Stats ---")

    scores = df["score"].values

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)

    print(f"Mean score   : {mean_score:.2f}")
    print(f"Median score : {median_score:.2f}")
    print(f"Std deviation: {std_score:.2f}")
    print(f"Max score    : {max_score}")
    print(f"Min score    : {min_score}")

    # Category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()

    print(f"\nMost stories in: {top_category} ({category_counts[top_category]} stories)")

    # Most commented story
    top_story = df.loc[df["num_comments"].idxmax()]

    print("\nMost commented story:")
    print(f"\"{top_story['title']}\" — {top_story['num_comments']} comments")

    # -----------------------------------------
    # Step 3: Add New Columns
    # -----------------------------------------

    # Engagement = comments per upvote
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # Popular if score > average score
    df["is_popular"] = df["score"] > avg_score

    # -----------------------------------------
    # Step 4: Save analysed data
    # -----------------------------------------
    output_path = "data/trends_analysed.csv"

    df.to_csv(output_path, index=False)

    print(f"\nSaved to {output_path}")


# Run program
if __name__ == "__main__":
    main()