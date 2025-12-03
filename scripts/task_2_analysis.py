from sqlalchemy import create_engine
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# --- DATABASE CONNECTION ---
DB_USER = "postgres"
DB_PASS = "1234beko"
DB_HOST = "localhost"
DB_NAME = "bank_reviews"

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')

# --- LOAD REVIEWS ---
df = pd.read_sql("SELECT review_id, review_text, bank_id FROM reviews", engine)
print(f"Loaded {len(df)} reviews.")

# --- SENTIMENT ANALYSIS ---
analyzer = SentimentIntensityAnalyzer()
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

df['sentiment_label'], df['sentiment_score'] = zip(*df['review_text'].apply(get_sentiment))

# --- UPDATE DATABASE ---
df[['sentiment_label', 'sentiment_score', 'review_id']].to_sql(
    'reviews',
    engine,
    if_exists='replace',  # or 'append' + careful update logic
    index=False
)
print("Sentiment analysis updated via SQLAlchemy.")

# --- THEME EXTRACTION ---
df['cleaned'] = df['review_text'].str.lower().str.replace(r'[^a-z0-9\s]', '', regex=True)

vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=100)
X = vectorizer.fit_transform(df['cleaned'])
feature_names = vectorizer.get_feature_names_out()

themes = {}
for bank_id in df['bank_id'].unique():
    bank_texts = df[df['bank_id']==bank_id]['cleaned']
    vector = vectorizer.transform(bank_texts)
    summed = vector.sum(axis=0)
    keywords_scores = [(feature_names[i], summed[0,i]) for i in range(len(feature_names))]
    keywords_scores.sort(key=lambda x: x[1], reverse=True)
    themes[int(bank_id)] = [kw for kw, score in keywords_scores[:10]]

print("\nTop keywords/themes per bank:")
bank_df = pd.read_sql("SELECT bank_id, bank_name FROM banks", engine)
for bank_id, keywords in themes.items():
    bank_name = bank_df[bank_df['bank_id']==bank_id]['bank_name'].values[0]
    print(f"{bank_name}: {keywords}")