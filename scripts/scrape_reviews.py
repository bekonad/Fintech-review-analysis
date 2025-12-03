"""
scrape_reviews.py
-----------------
Scrapes reviews for three Ethiopian banks and saves them to CSV.
Optionally, integrates preprocessing to produce cleaned_reviews.csv.
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import logging
from datetime import datetime
import subprocess

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# -------------------------
# Configuration
# -------------------------
APPS = [
    {"name": "Commercial Bank of Ethiopia", "id": "com.combanketh.mobilebanking"},
    {"name": "Bank of Abyssinia", "id": "com.boa.boaMobileBanking"},
    {"name": "Dashen Bank", "id": "com.dashen.dashensuperapp"}
]

REVIEWS_PER_APP = 400
RAW_OUTPUT_CSV = "data/raw/reviews.csv"


# -------------------------
# Scraping Function
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
        logging.error(f"Could not scrape {app_name}: {e}")
        return []

# -------------------------
# Main Script
# -------------------------
def main():
    all_reviews = []

    for app in APPS:
        logging.info(f"Scraping reviews for {app['name']}...")
        app_reviews = scrape_app_reviews(app["id"], app["name"])
        all_reviews.extend(app_reviews)

    df = pd.DataFrame(all_reviews)
    logging.info(f"Collected {len(df)} reviews.")

    # Save raw CSV
    df.to_csv(RAW_OUTPUT_CSV, index=False)
    logging.info(f"Saved raw reviews to {RAW_OUTPUT_CSV}")

    # Optional: Run preprocessing automatically
    try:
        subprocess.run(["python", "scripts/preprocess.py"], check=True)
        logging.info("Preprocessing complete. Cleaned CSV saved.")
    except Exception as e:
        logging.error(f"Could not run preprocessing: {e}")

if __name__ == "__main__":
    main()