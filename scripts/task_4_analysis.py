# scripts/task_4_analysis.py

# --- IMPORT LIBRARIES ---
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
import yaml

# --- STEP 0: LOAD CONFIG AND CREATE FIGURES DIRECTORY ---
with open('config.yaml') as f:
    config = yaml.safe_load(f)

DB_USER = config['db_user']
DB_PASS = config['db_pass']
DB_HOST = config['db_host']
DB_NAME = config['db_name']

if not os.path.exists("figures"):
    os.makedirs("figures")

# --- STEP 1: LOAD DATA ---
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')

# Load reviews and banks from PostgreSQL
reviews = pd.read_sql("SELECT * FROM reviews", engine)
banks = pd.read_sql("SELECT * FROM banks", engine)

# Load top keywords/themes CSV
themes = pd.read_csv("data/bank_themes.csv")

# Quick check
print("Reviews sample:")
print(reviews.head())
print("\nThemes sample:")
print(themes.head())

# --- STEP 2: IDENTIFY DRIVERS AND PAIN POINTS ---
drivers = {}
pain_points = {}

for bank_id in reviews['bank_id'].unique():
    bank_reviews = reviews[reviews['bank_id'] == bank_id]
    
    # Drivers: top positive review samples
    pos_reviews = bank_reviews[bank_reviews['sentiment_label'] == 'positive']
    drivers[bank_id] = pos_reviews['review_text'].sample(min(5, len(pos_reviews))).tolist()
    
    # Pain points: top negative review samples
    neg_reviews = bank_reviews[bank_reviews['sentiment_label'] == 'negative']
    pain_points[bank_id] = neg_reviews['review_text'].sample(min(5, len(neg_reviews))).tolist()

# --- STEP 3: ADD BANK NAMES ---
bank_mapping = dict(zip(banks['bank_id'], banks['bank_name']))
reviews['bank_name'] = reviews['bank_id'].map(bank_mapping)
themes['bank_name'] = themes['bank_id'].map(bank_mapping)

# Print for verification
print("\nDrivers per bank:")
for bank_id, texts in drivers.items():
    print(f"{bank_mapping[bank_id]}: {texts}")

print("\nPain points per bank:")
for bank_id, texts in pain_points.items():
    print(f"{bank_mapping[bank_id]}: {texts}")

# --- STEP 4: COMPARE BANKS (AVERAGE RATINGS AND SENTIMENT) ---
avg_ratings = reviews.groupby('bank_name')['rating'].mean()
avg_sentiment = reviews.groupby('bank_name')['sentiment_score'].mean()

print("\nAverage ratings per bank:")
print(avg_ratings)
print("\nAverage sentiment per bank:")
print(avg_sentiment)

# --- STEP 5: VISUALIZATIONS ---
# 1. Sentiment Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=reviews, x='bank_name', hue='sentiment_label')
plt.title("Sentiment Distribution per Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=15)
plt.savefig("figures/sentiment_distribution.png")
plt.show()

# 2. Rating Distribution
plt.figure(figsize=(8,5))
sns.boxplot(data=reviews, x='bank_name', y='rating')
plt.title("Rating Distribution per Bank")
plt.xlabel("Bank")
plt.ylabel("Rating")
plt.xticks(rotation=15)
plt.savefig("figures/rating_distribution.png")
plt.show()

# 3. Keyword Clouds per Bank
for idx, row in themes.iterrows():
    bank_name = row['bank_name']
    keywords_text = row['top_keywords']
    
    # Skip if empty
    if not isinstance(keywords_text, str) or keywords_text.strip() == "":
        continue
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(keywords_text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Top Keywords – {bank_name}")
    plt.savefig(f"figures/keyword_cloud_{bank_name}.png")
    plt.show()

# 4. Average Rating and Sentiment per Bank
# Average Rating per Bank
plt.figure(figsize=(8,5))
sns.barplot(x=avg_ratings.index, y=avg_ratings.values, palette="Blues_d")
plt.title("Average Rating per Bank")
plt.xlabel("Bank")
plt.ylabel("Average Rating")
plt.ylim(0,5)
plt.xticks(rotation=15)  # optional: rotate names for readability
plt.savefig("figures/average_rating_per_bank.png")
plt.show()

# Average Sentiment per Bank
plt.figure(figsize=(8,5))
sns.barplot(x=avg_sentiment.index, y=avg_sentiment.values, palette="Greens_d")
plt.title("Average Sentiment Score per Bank")
plt.xlabel("Bank")
plt.ylabel("Average Sentiment Score")
plt.ylim(0,1)
plt.xticks(rotation=15)
plt.savefig("figures/average_sentiment_per_bank.png")
plt.show()

# --- STEP 6: RECOMMENDATIONS ---
print("\n--- Recommendations per Bank ---")
recommendations = {}

for bank_id in reviews['bank_id'].unique():
    bank_name = bank_mapping[bank_id]
    driver_examples = drivers[bank_id][:2] if len(drivers[bank_id]) >= 2 else drivers[bank_id]
    pain_examples = pain_points[bank_id][:2] if len(pain_points[bank_id]) >= 2 else pain_points[bank_id]
    
    # Example recommendation logic
    recs = []
    if any("login" in text.lower() or "error" in text.lower() for text in pain_examples):
        recs.append("Improve login reliability")
    if any("slow" in text.lower() or "lag" in text.lower() for text in pain_examples):
        recs.append("Optimize app speed and response time")
    if any("crash" in text.lower() for text in pain_examples):
        recs.append("Fix app stability issues")
    if len(recs) == 0:
        recs.append("Maintain current strengths")
    
    recommendations[bank_name] = {
        "drivers": driver_examples,
        "pain_points": pain_examples,
        "recommendations": recs
    }

# Print recommendations
for bank, info in recommendations.items():
    print(f"\nBank: {bank}")
    print(f"Drivers: {info['drivers']}")
    print(f"Pain Points: {info['pain_points']}")
    print(f"Recommendations: {info['recommendations']}")

# --- STEP 7: SAVE RECOMMENDATIONS CSV ---
rec_data = []
for bank, info in recommendations.items():
    rec_data.append({
        "bank_name": bank,
        "drivers": " | ".join(info['drivers']),
        "pain_points": " | ".join(info['pain_points']),
        "recommendations": " | ".join(info['recommendations'])
    })

df_recommendations = pd.DataFrame(rec_data)
df_recommendations.to_csv("data/bank_recommendations.csv", index=False)
print("\nRecommendations saved to data/bank_recommendations.csv")

# --- STEP 7: ETHICS / REVIEW BIAS NOTE ---
print("\n--- Review Bias Note ---")
print("The review dataset may contain a negative skew, as dissatisfied users are more likely to leave reviews.")
print("Additionally, review counts per rating are uneven, which can influence average sentiment and rating metrics.")
print("This should be considered when interpreting insights and recommendations.")