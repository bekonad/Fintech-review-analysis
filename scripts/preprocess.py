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

