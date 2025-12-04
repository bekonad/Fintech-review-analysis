"""
preprocess.py
-------------
Cleans raw scraped Google Play reviews before analysis.

Tasks performed:
- Remove duplicates
- Remove missing values
- Normalize dates (YYYY-MM-DD)
- Clean text (lowercase, remove noise)
- Validate rating values (1–5)
- Standardize bank names
- Save cleaned file

Input:  reviews.csv
Output: cleaned_reviews.csv
"""

import pandas as pd
import re
import logging
import yaml

# Load config
with open('config.yaml') as f:
    config = yaml.safe_load(f)

INPUT_FILE = "data/raw/reviews.csv"
OUTPUT_FILE = "data/cleaned_reviews.csv"


# -------------------------------------------------------
# Logging Setup
# -------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

# -------------------------------------------------------
# Text Cleaning
# -------------------------------------------------------
def clean_text(text):
    """Normalize text: lowercase, remove URLs, remove symbols, trim spaces."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)            # remove URLs
    text = re.sub(r"[^a-z0-9.,!? ]", " ", text)           # remove emojis/symbols
    text = re.sub(r"\s+", " ", text)                      # remove extra spaces
    return text.strip()

# -------------------------------------------------------
# Bank Name Normalization
# -------------------------------------------------------
def standardize_bank_name(bank):
    bank = str(bank).lower()
    if "commercial bank" in bank or "cbe" in bank:
        return "Commercial Bank of Ethiopia"
    if "abyssinia" in bank or "boa" in bank:
        return "Bank of Abyssinia"
    if "dashen" in bank:
        return "Dashen Bank"
    return bank.title()
# -------------------------------------------------------
# Main Preprocessing
# -------------------------------------------------------
def preprocess_reviews(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    logging.info(f"Loading raw reviews from {input_file}")
    df = pd.read_csv(input_file)

    logging.info("Dropping duplicates")
    df = df.drop_duplicates()

    logging.info("Normalizing dates")
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

    logging.info("Cleaning review text")
    df['review'] = df['review'].apply(clean_text)

    logging.info("Removing empty reviews")
    df = df[df['review'].str.strip() != ""]

    logging.info("Validating ratings (1–5)")
    df = df[df['rating'].between(1,5)]

    logging.info("Standardizing bank names")
    df['bank'] = df['bank'].apply(standardize_bank_name)

    logging.info(f"Saving cleaned reviews to {output_file}")
    df.to_csv(output_file, index=False)
    logging.info("Preprocessing complete")
    return df

# -------------------------------------------------------
# Run preprocessing if called directly
# -------------------------------------------------------
if __name__ == "__main__":
    preprocess_reviews()
