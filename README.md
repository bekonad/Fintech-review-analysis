Task 1 — Data Collection & Preprocessing
Objective

Collect at least 400+ reviews per bank (CBE, BOA, Dashen) from Google Play Store, clean the dataset, and prepare it for sentiment/thematic analysis.

Tools Used

google-play-scraper — to fetch reviews programmatically

Pandas — preprocessing (cleaning, deduplication, formatting)

Python 3.10+

Git & GitHub — version control and project organization

Scraping Methodology

Used google_play_scraper.reviews() to collect:

Review text

Rating (1–5 stars)

Review date

Bank/app name

Source

Targeted 400+ reviews per app, resulting in:

1,200 raw reviews collected

1,189 cleaned after removing duplicates and handling missing values

Preprocessing Steps

✔ Removed duplicate reviews using:

df.drop_duplicates(subset=["review", "date", "bank"])


✔ Ensured no missing values in critical fields (review, rating)
✔ Normalized date formats to YYYY-MM-DD using:

pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")


✔ Saved final dataset as:

reviews.csv

Folder Structure
Fintech Review Analysis/
│
├── scrape_reviews.py         # Scraping + cleaning script
├── reviews.csv                # Cleaned reviews (1189 rows)
├── requirements.txt
├── .gitignore
├── README.md
└── venv/                      # Virtual environment (ignored by git)

How to Run the Scraper

# activate virtual environment

& .\venv\Scripts\Activate.ps1

# install dependencies

pip install -r requirements.txt

# run scraper 

python scrape_reviews.py

Next Steps (Task 2)

Perform sentiment analysis using DistilBERT

Extract keywords using TF-IDF and spaCy

Assign themes to reviews

Output: reviews_processed.csv

Task 2 — Sentiment & Thematic Analysis
Objective

Analyze user reviews to understand emotional tone (sentiment), extract important keywords, and group feedback into high-level themes for each bank.

Methods
1. Sentiment Analysis

Model used:

distilbert-base-uncased-finetuned-sst-2-english (Hugging Face)

Pipeline:

Each review passed to the DistilBERT sentiment classifier

Extracted:

sentiment_label (Positive, Negative, Neutral)

sentiment_score (confidence score)

Goal achieved ✔: sentiment for 100% of reviews.

2. Keyword Extraction

Used:

spaCy noun chunks

OR fallback: TF-IDF

Example extracted keywords:

"login issue", "slow transfer", "UI design", "network error", "customer support"

3. Thematic Clustering

Keywords were grouped into 5 major themes:

Theme	Description
Account Access Issues	login, password, reset errors
Transaction Performance	transfer delays, slow processing
User Interface & Experience	design, navigation, layout
Customer Support	help, agent support, problems not solved
Feature Related Requests	fingerprint login, dark mode, alerts

Theme assignment added as column:

identified_theme

Output File
reviews_processed.csv


Columns include:

review

rating

date

bank

sentiment_label

sentiment_score

keywords

identified_theme

KPIs Achieved
KPI	Result
Sentiment scores for 90%+ reviews	100% completed
Extract 3+ themes per bank	5 total themes extracted
Modular pipeline	Yes
Examples of themes visible	Yes (keywords + themes)
How to Run Task 2 Script
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python task_2_sentiment_thematic_analysis.py