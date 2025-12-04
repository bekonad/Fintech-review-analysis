# scripts/task_4_analysis.py

# --- IMPORT LIBRARIES ---
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# --- STEP 0: CREATE FIGURES DIRECTORY ---
if not os.path.exists("figures"):
    os.makedirs("figures")

# --- STEP 1: LOAD DATA ---
DB_USER = "postgres"
DB_PASS = "1234beko"
DB_HOST = "localhost"
DB_NAME = "bank_reviews"

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

# Print for verification
print("\nDrivers per bank:")
for bank_id, texts in drivers.items():
    bank_name = banks[banks['bank_id']==bank_id]['bank_name'].values[0]
    print(f"{bank_name}: {texts}")

print("\nPain points per bank:")
for bank_id, texts in pain_points.items():
    bank_name = banks[banks['bank_id']==bank_id]['bank_name'].values[0]
    print(f"{bank_name}: {texts}")

# --- STEP 3: COMPARE BANKS (AVERAGE RATINGS AND SENTIMENT) ---
avg_ratings = reviews.groupby('bank_id')['rating'].mean()
avg_sentiment = reviews.groupby('bank_id')['sentiment_score'].mean()

print("\nAverage ratings per bank:")
print(avg_ratings)
print("\nAverage sentiment per bank:")
print(avg_sentiment)

# --- STEP 4: VISUALIZATIONS ---

# 1. Sentiment Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=reviews, x='bank_id', hue='sentiment_label')
plt.title("Sentiment Distribution per Bank")
plt.xlabel("Bank ID")
plt.ylabel("Number of Reviews")
plt.savefig("figures/sentiment_distribution.png")
plt.show()

# 2. Rating Distribution
plt.figure(figsize=(8,5))
sns.boxplot(data=reviews, x='bank_id', y='rating')
plt.title("Rating Distribution per Bank")
plt.xlabel("Bank ID")
plt.ylabel("Rating")
plt.savefig("figures/rating_distribution.png")
plt.show()

# 3. Keyword Clouds per Bank
for idx, row in themes.iterrows():
    bank_id = row['bank_id']
    bank_name = banks[banks['bank_id']==bank_id]['bank_name'].values[0]
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

# --- STEP 4b: OPTIONAL COMPARISON PLOTS ---

# Average Rating per Bank
plt.figure(figsize=(8,5))
sns.barplot(x=avg_ratings.index, y=avg_ratings.values, palette="Blues_d")
plt.title("Average Rating per Bank")
plt.xlabel("Bank ID")
plt.ylabel("Average Rating")
plt.ylim(0,5)
plt.savefig("figures/average_rating_per_bank.png")
plt.show()

# Average Sentiment per Bank
plt.figure(figsize=(8,5))
sns.barplot(x=avg_sentiment.index, y=avg_sentiment.values, palette="Greens_d")
plt.title("Average Sentiment Score per Bank")
plt.xlabel("Bank ID")
plt.ylabel("Average Sentiment Score")
plt.ylim(0,1)
plt.savefig("figures/average_sentiment_per_bank.png")
plt.show()

# --- STEP 5: RECOMMENDATIONS ---
print("\n--- Recommendations per Bank ---")
recommendations = {}

for bank_id in reviews['bank_id'].unique():
    bank_name = banks[banks['bank_id']==bank_id]['bank_name'].values[0]
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

# --- STEP 6: SAVE RECOMMENDATIONS CSV ---
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