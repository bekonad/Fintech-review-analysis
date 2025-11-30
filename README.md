# Customer Experience Analytics – Fintech Apps

This project scrapes, preprocesses, and analyzes Google Play Store reviews for three Ethiopian banks. It is part of the **Week 2 Challenge at 10 Academy: Artificial Intelligence Mastery**.

---

## Banks Analyzed
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

---

## Project Structure
    -
    ├── scrape_reviews.py # Scrapes reviews from Google Play Store
    ├── preprocess.py # Cleans and normalizes scraped reviews
    ├── reviews.csv # Raw scraped reviews (optional, large)
    ├── cleaned_reviews.csv # Fully cleaned dataset, ready for analysis
    ├── task_2_sentiment_thematic_analysis.py # Sentiment & thematic analysis (Task 2)
    ├── reviews_processed.csv # Processed dataset with sentiment labels, scores, keywords, and themes
    ├── requirements.txt # Python dependencies
    ├── .gitignore # Excludes large or temporary files
    └── README.md # Project documentation                         


---

## Workflow

### 1. Scraping Reviews (Task 1)
Run `scrape_reviews.py` to collect reviews from the three bank apps.  

- Saves raw reviews to `reviews.csv`  
- Automatically runs `preprocess.py` to produce `cleaned_reviews.csv`  

```bash
python scrape_reviews.py
```
Output: reviews.csv — ready for analysis.

---

### 2. Preprocessing

- Cleans raw review data:

- Removes duplicates and missing values

- Normalizes dates (YYYY-MM-DD)

- Validates rating values (1–5)

- Cleans text (lowercase, remove URLs, symbols, extra spaces)

- Standardizes bank names

```bash
python preprocess.py
```
Output: cleaned_reviews.csv — ready for analysis.

--- 


### 3. Analysis (Task 2)

Use cleaned_reviews.csv for:

 - Sentiment Analysis: Hugging Face DistilBERT (preferred), optional VADER/TextBlob fallback

 - Keyword Extraction: spaCy noun chunks or TF-IDF

 - Thematic Clustering: Assign reviews into 5 main themes:

    - Account Access Issues

    - Transaction Performance

    - User Interface & Experience

    - Customer Support

    - Feature / Others

 - Identify satisfaction drivers and pain points

```bash
python task_2_sentiment_thematic_analysis.py
```
Files Involved:

    - task_2_sentiment_thematic_analysis.py – Analysis script for sentiment and themes

    - reviews_processed.csv – Processed dataset with sentiment labels, scores, keywords, and identified themes

- ** Output: reviews_processed.csv — includes sentiment labels, scores, keywords, and identified themes.**

---

### Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Main packages:

    google-play-scraper – Web scraping

    pandas – Data manipulation

    numpy – Numerical operations

    regex – Text cleaning

    logging – Standard logging

    Optional / Task 2 packages:

    transformers – Hugging Face sentiment models

    spacy – NLP processing

    torch – Required for Transformers

    vaderSentiment – Simple sentiment analysis (optional)
---

## Output Files

| File                   | Description                                                      |
|------------------------|------------------------------------------------------------------|
| `reviews.csv`          | Raw scraped reviews                                              |
| `cleaned_reviews.csv`  | Preprocessed and cleaned reviews                                 |
| `reviews_processed.csv`| Reviews with sentiment labels, scores, keywords, and themes      |

---

Use reviews_processed.csv for all downstream analysis, visualization, and insight tasks.

---

GitHub Branching Strategy

- task-1 – Scraping and preprocessing

- task-2 – Sentiment and thematic analysis

- main – Final merged version including scripts and CSVs
  
---
Next Steps

Task 3: Store cleaned_reviews.csv in PostgreSQL database

Task 4: Generate visualizations and insights for stakeholders


---
