"""
preprocess.py
-------------
Preprocesses raw scraped Google Play reviews:
- removes duplicates
- handles missing values
- normalizes dates
- optional text cleaning
Outputs: cleaned_reviews.csv
"""

import pandas as pd
import re

INPUT_FILE = "reviews.csv"
OUTPUT_FILE = "cleaned_reviews.csv"


def clean_text(text):
    """Basic text normalization."""
    if not isinstance(text, str):
        return text
    text = text.lower()
    text = re.sub(r"\s+", " ", text)       # remove extra spaces
    text = re.sub(r"[^a-z0-9.,!? ]", "", text)  # keep letters, numbers & punctuation
    return text.strip()


def preprocess_reviews(df):
    """Perform cleaning steps on the reviews DataFrame."""
    print("Initial rows:", len(df))

    # Drop missing essential values
    df = df.dropna(subset=["review", "rating"])

    # Remove duplicates
    df = df.drop_duplicates(subset=["review", "date", "bank"])

    # Normalize dates
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # Clean text
    df["review"] = df["review"].apply(clean_text)

    print("Final rows after cleaning:", len(df))
    print("Missing values:\n", df.isnull().sum())

    return df


def main():
    print("Loading dataset...")
    df = pd.read_csv(INPUT_FILE)

    df_clean = preprocess_reviews(df)

    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"Cleaned dataset saved as {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
