# Fintech App Review Analysis – Week 2 Final Report

## Project Overview
This project analyzes user reviews of three Ethiopian banks' mobile apps to provide actionable insights for improving customer experience. It demonstrates a full data analytics workflow, from web scraping to NLP analysis, database storage, visualization, and recommendation generation.

**Banks analyzed:**
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

**Project Goals:**
1. Collect and preprocess at least 1,200 user reviews.
2. Analyze review sentiment and extract recurring themes.
3. Identify key satisfaction drivers and pain points per bank.
4. Store processed data in a PostgreSQL database.
5. Generate actionable insights and visualizations for stakeholders.

**Project Date:** 26 Nov – 02 Dec 2025

---

## File structure

Fintech Review Analysis/
├── .github/
├── data/
│   ├── raw/
│   │   └── reviews.csv
│   ├── bank_recommendations.csv
│   ├── bank_themes.csv
│   ├── cleaned_reviews.csv
│   └── reviews_processed.csv
├── figures/
│   ├── average_rating_per_bank.png
│   ├── average_sentiment_per_bank.png
│   ├── keyword_cloud_Bank of Abyssinia.png
│   ├── keyword_cloud_Commercial Bank of Ethiopia.png
│   ├── keyword_cloud_Dashen Bank.png
│   ├── rating_distribution.png
│   └── sentiment_distribution.png
├── notebooks/
├── reports/
├── scripts/
│   ├── insert_reviews.py
│   ├── preprocess.py
│   ├── scrape_reviews.py
│   ├── sentiment_analysis.py
│   ├── task_2_analysis.py
│   ├── task_2_sentiment_thematic_analysis.py
│   └── task_4_analysis.py
├── sql/
├── tests/
├── venv/
├── visualizations/
├── .gitignore
├── README.md
└── requirements.txt

## Project Tasks & Methodology

### Task 1: Data Collection & Preprocessing
**Objective:** Gather user reviews and clean the dataset for analysis.

**Steps Taken:**
- Used `google-play-scraper` to scrape reviews, ratings, posting dates, and app names for each bank.
- Targeted at least 400 reviews per bank, totaling 1,189 reviews.
- Cleaned the dataset by:
  - Removing duplicates
  - Handling missing data
  - Normalizing dates to `YYYY-MM-DD`
- Saved the cleaned dataset as `data/cleaned_reviews.csv`.

**Key Outputs:**
- `cleaned_reviews.csv`: cleaned, ready-to-analyze review dataset.
- Methodology and preprocessing steps documented for reproducibility.

---

### Task 2: Sentiment & Thematic Analysis
**Objective:** Quantify user sentiment and identify recurring themes.

**Steps Taken:**
1. **Sentiment Analysis**
   - Used DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`) to classify reviews into `positive`, `negative`, and `neutral`.
   - Aggregated sentiment scores per bank to understand overall customer satisfaction.

2. **Thematic Analysis**
   - Extracted significant keywords using TF-IDF.
   - Clustered keywords manually into 3–5 themes per bank (e.g., "Login Issues", "Transaction Speed", "User Interface").
   - Saved processed reviews with sentiment and themes as `reviews_processed.csv`.
   - Extracted top keywords per bank and saved as `bank_themes.csv`.

**Key Outputs:**
- `reviews_processed.csv`: includes `review_text`, `rating`, `sentiment_label`, `sentiment_score`, and `identified_theme`.
- `bank_themes.csv`: top keywords/themes for each bank.

---

### Task 3: Store Data in PostgreSQL
**Objective:** Implement a persistent storage solution for processed review data.

**Steps Taken:**
- Created a PostgreSQL database named `bank_reviews`.
- Defined two tables:
  1. **banks**: `bank_id`, `bank_name`, `app_name`
  2. **reviews**: `review_id`, `bank_id`, `review_text`, `rating`, `review_date`, `sentiment_label`, `sentiment_score`, `source`
- Inserted cleaned review data using Python (`SQLAlchemy` + `psycopg2`).
- Verified data integrity via SQL queries:
  - Count of reviews per bank
  - Average ratings and sentiment scores per bank

**Key Outputs:**
- Fully functional database storing >1,000 reviews.
- Ensures reproducibility and query-based analysis.

---

### Task 4: Insights & Recommendations
**Objective:** Derive actionable insights from reviews and visualize results for stakeholders.

**Steps Taken:**

1. **Drivers & Pain Points**
   - Sampled top 5 positive reviews per bank → **drivers**.
   - Sampled top 5 negative reviews per bank → **pain points**.
   - Identified examples such as:
     - Drivers: "Fast transfers", "Easy-to-use interface"
     - Pain Points: "Login errors", "Slow loading", "Crashes"

2. **Recommendations**
   - Generated per bank based on pain points:
     - Improve login reliability
     - Optimize app speed and response time
     - Fix app stability issues
     - Maintain current strengths when no major issues

3. **Visualizations**
   - Sentiment distribution per bank
   - Rating distribution per bank
   - Keyword clouds per bank
   - Optional bar charts: average rating per bank, average sentiment per bank
   - All figures saved in the `figures/` directory.

4. **Ethics / Review Bias**
   - Noted that reviews may be negatively skewed, as dissatisfied users are more likely to leave reviews.
   - Uneven review counts per rating may influence aggregate sentiment.

**Key Outputs:**
- `bank_recommendations.csv` with drivers, pain points, and recommendations.
- Figures in `figures/` for report visualization.

---

## Usage Instructions

1. **Install dependencies**
```bash
pip install -r requirements.txt

2. Setup Database

- Ensure PostgreSQL is installed and running.

- Update database credentials in task_4_analysis.py as needed.

- Run Script

python scripts/task_1_scrape_preprocess.py
python scripts/task_2_analysis.py
python scripts/task_4_analysis.py

Outputs

CSVs in data/

Figures in figures/

Recommendations CSV in data/bank_recommendations.csv

Notes

Compatible with Python 3.x.

Review datasets may contain bias (negative skew, uneven rating counts).

All scripts are modular and documented for reproducibility.

Author

- Bereket Feleke

- Omega Consultancy – Week 2 Project

- Project Date: 26 Nov – 02 Dec 2025