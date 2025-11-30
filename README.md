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