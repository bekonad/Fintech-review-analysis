# Google Play Store Review Scraper
# Scrapes reviews for three Ethiopian banks and saves cleaned data to CSV

from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime

# -------------------------
# Configuration
# -------------------------
APPS = [
    {"name": "Commercial Bank of Ethiopia", "id": "com.combanketh.mobilebanking"},
    {"name": "Bank of Abyssinia", "id": "com.boa.boaMobileBanking"},
    {"name": "Dashen Bank", "id": "com.dashen.dashensuperapp"}
]

REVIEWS_PER_APP = 400
OUTPUT_CSV = "reviews.csv"

# -------------------------
# Functions
# -------------------------
def scrape_app_reviews(app_id, app_name, count=REVIEWS_PER_APP):
    """Scrape reviews for a single app."""
    try:
        result, _ = reviews(
            app_id,
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=count
        )
        reviews_list = []
        for r in result:
            reviews_list.append({
                "review": r["content"],
                "rating": r["score"],
                "date": r["at"].strftime("%Y-%m-%d"),
                "bank": app_name,
                "source": "Google Play"
            })
        return reviews_list
    except Exception as e:
        print(f"[ERROR] Could not scrape {app_name}: {e}")
        return []

def preprocess_reviews(df):
    """Clean the scraped reviews."""
    df = df.drop_duplicates(subset=["review", "date", "bank"])
    df = df.dropna(subset=["review", "rating"])
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df

# -------------------------
# Main Script
# -------------------------
def main():
    all_reviews = []

    for app in APPS:
        print(f"Scraping reviews for {app['name']}...")
        app_reviews = scrape_app_reviews(app["id"], app["name"])
        all_reviews.extend(app_reviews)

    df = pd.DataFrame(all_reviews)
    print(f"Collected {len(df)} reviews before cleaning.")

    # Clean data
    df = preprocess_reviews(df)
    print(f"Total reviews after cleaning: {len(df)}")
    print(f"Missing data:\n{df.isnull().sum()}")

    # Save to CSV
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved cleaned reviews to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()