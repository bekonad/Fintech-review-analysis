# insert_reviews.py
import pandas as pd
import psycopg2
from psycopg2 import sql

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASS = "1234beko"  # Replace with your actual password
CSV_PATH = "C:/Users/JERUSALEM/Desktop/10 ACA/Fintech review analysis/data/cleaned_reviews.csv"

# --- READ CSV ---
df = pd.read_csv(CSV_PATH)

# Ensure column names match your CSV
# Expected columns: review, rating, date, bank, source, sentiment_label, sentiment_score
print("CSV loaded. Sample data:")
print(df.head())

# --- CONNECT TO POSTGRES ---
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# --- HELPER: Get bank_id by bank name ---
def get_bank_id(bank_name):
    cur.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (bank_name,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        # Optional: Insert new bank if not exist
        cur.execute("INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) RETURNING bank_id",
                    (bank_name, bank_name + " Mobile App"))
        conn.commit()
        return cur.fetchone()[0]

# --- INSERT REVIEWS ---
for index, row in df.iterrows():
    bank_id = get_bank_id(row['bank'])
    cur.execute(
        """
        INSERT INTO reviews 
        (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            bank_id,
            row['review'],
            int(row['rating']),
            row['date'],
            row.get('sentiment_label', None),
            float(row.get('sentiment_score', 0)),
            row.get('source', 'Google Play')
        )
    )

# --- COMMIT & CLOSE ---
conn.commit()
cur.close()
conn.close()
print("All reviews inserted successfully!")