# scripts/insert_reviews.py
import pandas as pd
import psycopg2
import yaml

# ---Load config---
with open('config.yaml') as f:
    config = yaml.safe_load(f)

DB_HOST = config['db_host']
DB_NAME = config['db_name']
DB_USER = config['db_user']
DB_PASS = config['db_pass']
CSV_PATH = config['csv_path']

# --- LOAD CSV ---
df = pd.read_csv(CSV_PATH)
print(f"CSV loaded: {len(df)} reviews.")

# --- CONNECT TO DATABASE ---
conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
)
cur = conn.cursor()

# --- CREATE TABLES IF NOT EXIST ---
cur.execute("""
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name TEXT UNIQUE NOT NULL,
    app_name TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label TEXT,
    sentiment_score FLOAT,
    source TEXT
);
""")
conn.commit()
print("Tables verified or created.")


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