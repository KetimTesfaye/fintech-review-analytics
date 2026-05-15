import psycopg2
import pandas as pd
import os

# --- Step 1: Configuration ---
# host: "localhost" (your PC)
# user: "postgres" (the default admin)
# password: "admin123" (your secret key)
DB_CONFIG = {
    "host": "localhost",
    "database": "bank_reviews",
    "user": "postgres", 
    "password": "admin123" 
}

def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Create Banks table (The "Parent" table)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(100) UNIQUE NOT NULL,
            app_name VARCHAR(100)
        );
    """)

    # Create Reviews table (The "Child" table)
    # bank_id links back to the banks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            review_id VARCHAR(255) UNIQUE NOT NULL,
            bank_id INTEGER REFERENCES banks(bank_id),
            review_text TEXT,
            rating INTEGER,
            review_date DATE,
            sentiment_label VARCHAR(20),
            sentiment_score NUMERIC(5,4),
            identified_theme VARCHAR(100)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Step 2: Tables created successfully.")

create_tables() # Run this function

# --- Step 3: Load Data ---
csv_path = 'data/processed/sentiment_results.csv'

if os.path.exists(csv_path):
    df_reviews = pd.read_csv(csv_path)
    print(f"✅ Step 3: Loaded {len(df_reviews)} reviews from CSV.")
else:
    print(f"❌ Error: {csv_path} not found!")

    def insert_data(df):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 1. Insert unique banks into the banks table
    unique_banks = df['bank'].unique()
    for bank in unique_banks:
        cur.execute("""
            INSERT INTO banks (bank_name, app_name)
            VALUES (%s, %s)
            ON CONFLICT (bank_name) DO NOTHING;
        """, (bank, bank))
    
    conn.commit() # Save banks so they get IDs

    # 2. Get the new Bank IDs from the DB to link the reviews
    cur.execute("SELECT bank_id, bank_name FROM banks;")
    bank_map = {name: b_id for b_id, name in cur.fetchall()}

    # 3. Insert Reviews
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (review_id) DO NOTHING;
        """, (
            row['review_id'], 
            bank_map[row['bank']], 
            row['review_text'], 
            int(row['rating']), 
            row['review_date'],
            row['sentiment_label'],
            row['sentiment_score'],
            row['identified_theme']
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("🚀 Step 4: Data migration complete!")

# Run the final insertion
insert_data(df_reviews)