"""
task_2_sentiment_thematic_analysis.py
-------------------------------------
Task 2: Sentiment Analysis & Thematic Extraction for Fintech App Reviews
- Sentiment: Hugging Face DistilBERT (positive/negative)
- Keyword Extraction: spaCy noun chunks
- Theme Assignment: rule-based clustering
- Output: data/reviews_processed.csv
"""

import pandas as pd
from transformers import pipeline
import spacy
import logging

# -------------------------
# Config
# -------------------------
INPUT_FILE = "data/cleaned_reviews.csv"
OUTPUT_FILE = "data/reviews_processed.csv"

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# -------------------------
# Load NLP tools
# -------------------------
logging.info("Loading Hugging Face sentiment model...")
sentiment_analyzer = pipeline(
    "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1
)

logging.info("Loading spaCy model for keyword extraction...")
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logging.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    raise

# -------------------------
# Functions
# -------------------------
def analyze_sentiment(text):
    """Returns sentiment label and score using DistilBERT. Handles non-strings."""
    if not isinstance(text, str) or text.strip() == "":
        return "Neutral", 0.5
    result = sentiment_analyzer(text[:512])[0]
    return result["label"], result["score"]


def extract_keywords(text):
    """Extract noun chunks as keywords. Safely handle non-string values."""
    if not isinstance(text, str):
        text = ""
    doc = nlp(text.lower())
    keywords = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
    return ", ".join(keywords)


def assign_theme(keywords):
    """Assign review to a theme based on keywords"""
    keywords = keywords.lower()
    if any(k in keywords for k in ["login", "password", "account"]):
        return "Account Access Issues"
    elif any(k in keywords for k in ["transfer", "payment", "transaction", "slow"]):
        return "Transaction Performance"
    elif any(k in keywords for k in ["ui", "interface", "layout", "design"]):
        return "User Interface & Experience"
    elif any(k in keywords for k in ["support", "help", "customer"]):
        return "Customer Support"
    else:
        return "Feature / Others"


# -------------------------
# Main
# -------------------------
def main():
    logging.info(f"Loading data from {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)

    # Sentiment analysis
    logging.info("Analyzing sentiment...")
    df["sentiment_label"], df["sentiment_score"] = zip(*df["review"].apply(analyze_sentiment))

    # Keyword extraction
    logging.info("Extracting keywords...")
    df["keywords"] = df["review"].apply(extract_keywords)

    # Theme assignment
    logging.info("Assigning themes...")
    df["identified_theme"] = df["keywords"].apply(assign_theme)

    # Save processed dataset
    df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"Processed reviews saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()