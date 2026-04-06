# ---------------------------------------------
# TrendPulse - Task 4: Visualization
# ---------------------------------------------
# This script:
# 1. Loads analysed data
# 2. Creates 3 charts using matplotlib
# 3. Saves charts as PNG files
# 4. Creates a dashboard combining all charts
# ---------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os


def main():

    # Step 1: Load data
    file_path = "data/trends_analysed.csv"

    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return

    df = pd.read_csv(file_path)

    # Create outputs folder
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # -----------------------------------------
    # Chart 1: Top 10 Stories by Score
    # -----------------------------------------
    df_sorted = df.sort_values(by="score", ascending=False).head(10)

    # Shorten titles
    df_sorted["short_title"] = df_sorted["title"].apply(
        lambda x: x[:50] + "..." if len(x) > 50 else x
    )

    plt.figure()
    plt.barh(df_sorted["short_title"], df_sorted["score"])
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()

    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()

    # -----------------------------------------
    # Chart 2: Stories per Category
    # -----------------------------------------
    category_counts = df["category"].value_counts()

    plt.figure()
    plt.bar(category_counts.index, category_counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.savefig("outputs/chart2_categories.png")
    plt.close()

    # -----------------------------------------
    # Chart 3: Score vs Comments (Scatter)
    # -----------------------------------------
    plt.figure()

    # Split popular and non-popular
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.savefig("outputs/chart3_scatter.png")
    plt.close()

    # -----------------------------------------
    # Dashboard (Bonus)
    # -----------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Chart 1
    axes[0].barh(df_sorted["short_title"], df_sorted["score"])
    axes[0].set_title("Top Stories")
    axes[0].invert_yaxis()

    # Chart 2
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")

    # Chart 3
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    plt.suptitle("TrendPulse Dashboard")

    plt.savefig("outputs/dashboard.png")
    plt.close()

    print("All charts saved in outputs/ folder")


if __name__ == "__main__":
    main()