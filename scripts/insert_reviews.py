# scripts/insert_reviews.py
import pandas as pd
import psycopg2

# --- CONFIG ---
DB_HOST = "localhost"
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASS = "1234beko"
CSV_PATH = "data/cleaned_reviews.csv"

# --- LOAD CSV ---
df = pd.read_csv(CSV_PATH)
print(f"CSV loaded: {len(df)} reviews.")

# --- CONNECT TO DATABASE ---
conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
)
cur = conn.cursor()

# --- Insert Banks ---
banks = df['bank'].unique()
for bank in banks:
    cur.execute("""
        INSERT INTO banks (bank_name, app_name)
        VALUES (%s, %s)
        ON CONFLICT (bank_name) DO NOTHING;
    """, (bank, f"{bank} Mobile App"))
conn.commit()

# --- Helper: get bank_id ---
def get_bank_id(bank_name):
    cur.execute("SELECT bank_id FROM banks WHERE bank_name=%s", (bank_name,))
    return cur.fetchone()[0]

# --- Insert Reviews ---
for _, row in df.iterrows():
    bank_id = get_bank_id(row['bank'])
    cur.execute("""
        INSERT INTO reviews 
        (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        bank_id,
        row['review'],
        int(row['rating']),
        row['date'],
        row.get('sentiment_label', None),
        float(row.get('sentiment_score', 0)),
        row.get('source', 'Google Play')
    ))

conn.commit()
cur.close()
conn.close()
print("All reviews inserted successfully!")