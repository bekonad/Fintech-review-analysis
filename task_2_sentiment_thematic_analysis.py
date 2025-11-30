# Task 2: Sentiment and Thematic Analysis

import pandas as pd
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("reviews.csv")
print(f"Loaded {len(df)} reviews")

# -------------------------
# Sentiment Analysis
# -------------------------
# Using Hugging Face DistilBERT
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    try:
        result = sentiment_analyzer(text[:512])[0]  # Limit to 512 tokens for performance
        return result['label'], result['score']
    except:
        return "Neutral", 0.5

# Apply sentiment
df['sentiment_label'], df['sentiment_score'] = zip(*df['review'].apply(analyze_sentiment))

print("Sentiment analysis done!")

# -------------------------
# Thematic / Keyword Extraction
# -------------------------
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
    return ", ".join(keywords)

df['keywords'] = df['review'].apply(extract_keywords)

# Optional: cluster keywords into broader themes (example: rule-based)
def assign_theme(keywords):
    keywords = keywords.lower()
    if any(k in keywords for k in ['login', 'password', 'account']):
        return "Account Access Issues"
    elif any(k in keywords for k in ['transfer', 'payment', 'transaction', 'slow']):
        return "Transaction Performance"
    elif any(k in keywords for k in ['ui', 'interface', 'layout', 'design']):
        return "User Interface & Experience"
    elif any(k in keywords for k in ['support', 'help', 'customer']):
        return "Customer Support"
    else:
        return "Feature / Others"

df['identified_theme'] = df['keywords'].apply(assign_theme)

# -------------------------
# Save Processed Data
# -------------------------
df.to_csv("reviews_processed.csv", index=False)
print("Processed reviews saved to reviews_processed.csv")