import pandas as pd
from sqlalchemy import create_engine, text

# Connection setup
DATABASE_URL = 'postgresql://postgres:admin123@localhost:5432/bank_reviews'
engine = create_engine(DATABASE_URL)

def migrate_data():
    try:
        # 1. Load the processed Task 2 results
        df = pd.read_csv('data/processed/sentiment_results.csv')
        
        # 2. Check if Banks already exist to avoid UniqueViolation
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM banks"))
            count = result.scalar()
        
        if count == 0:
            print("Seeding banks table...")
            banks_data = [
                {'bank_name': 'CBE', 'app_name': 'CBE Birr'},
                {'bank_name': 'BOA', 'app_name': 'BOA Mobile'},
                {'bank_name': 'Dashen', 'app_name': 'Dashen Amole'}
            ]
            pd.DataFrame(banks_data).to_sql('banks', engine, if_exists='append', index=False)
        else:
            print("Banks already exist in database. Skipping seed step.")
        
        # 3. Map Bank Names to database Bank IDs
        db_banks = pd.read_sql('SELECT bank_id, bank_name FROM banks', engine)
        bank_map = dict(zip(db_banks['bank_name'], db_banks['bank_id']))
        df['bank_id'] = df['bank'].map(bank_map)
        
        # 4. Prepare and rename columns
        reviews_to_db = df[[
            'review_id', 'bank_id', 'review', 'rating', 
            'date', 'sentiment', 'confidence', 'theme', 'source'
        ]].copy()
        
        reviews_to_db.columns = [
            'review_id', 'bank_id', 'review_text', 'rating', 
            'review_date', 'sentiment_label', 'sentiment_score', 'identified_theme', 'source'
        ]
        
        # 5. Insert into PostgreSQL (using 'if_exists=append' to add to existing rows)
        # We use index=False because review_id is already in our dataframe
        reviews_to_db.to_sql('reviews', engine, if_exists='append', index=False, method='multi')
        print(f"✅ Successfully migrated {len(reviews_to_db)} reviews to PostgreSQL.")

    except Exception as e:
        print(f"❌ Error during migration: {e}")

if __name__ == "__main__":
    migrate_data()