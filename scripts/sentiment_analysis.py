# sentiment_analysis.py
import pandas as pd
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASS = "1234beko"  # Replace with your actual password

# --- CONNECT TO POSTGRES ---
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# --- LOAD REVIEWS ---
df = pd.read_sql("SELECT review_id, review_text FROM reviews", conn)
print(f"Loaded {len(df)} reviews.")

# --- INITIALIZE VADER ---
analyzer = SentimentIntensityAnalyzer()

# --- FUNCTION TO GET SENTIMENT ---
def get_sentiment(text):
    if not text:
        return "neutral", 0
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return "positive", compound
    elif compound <= -0.05:
        return "negative", compound
    else:
        return "neutral", compound

# --- ANALYZE AND UPDATE DATABASE ---
for index, row in df.iterrows():
    label, score = get_sentiment(row['review_text'])
    cur.execute(
        """
        UPDATE reviews
        SET sentiment_label = %s,
            sentiment_score = %s
        WHERE review_id = %s
        """,
        (label, score, row['review_id'])
    )

# --- COMMIT & CLOSE ---
conn.commit()
cur.close()
conn.close()
print("Sentiment analysis completed and database updated.")