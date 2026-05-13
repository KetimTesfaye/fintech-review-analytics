import pandas as pd
from google_play_scraper import Sort, reviews
import os

print("--- 🚀 Starting Task 1: Scraper & Preprocessor ---")

os.makedirs('data/raw', exist_ok=True)

target_apps = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp' 
}

for bank_name, app_id in target_apps.items():
    print(f"\n--- 🏦 Processing {bank_name} ---")
    
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=1000 
        )
        print(f"  📥 Scraped {len(result)} raw reviews.")
        
        bank_data = []
        for rev in result:
            bank_data.append({
                'id': rev['reviewId'],               
                'review': rev['content'],            # EXACT MATCH
                'rating': rev['score'],              # EXACT MATCH
                'date': rev['at'],                   # EXACT MATCH
                'bank': bank_name,                   # EXACT MATCH
                'source': 'Google Play'              # EXACT MATCH
            })
            
        df = pd.DataFrame(bank_data)
        
        # --- Preprocessing ---
        # 1. Remove duplicate reviews (id)
        initial_len = len(df)
        df = df.drop_duplicates(subset=['id'])
        print(f"  🧹 Removed {initial_len - len(df)} duplicates.")

        # 2. Handle missing values: drop rows missing review text or rating; document counts
        current_len = len(df)
        df = df.dropna(subset=['review', 'rating'])
        print(f"  🧹 Dropped {current_len - len(df)} rows missing text/rating.")

        # 3. Normalize dates to YYYY-MM-DD format
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # 4. Select final columns
        final_df = df[['review', 'rating', 'date', 'bank', 'source']]
        
        final_count = len(final_df)
        if final_count < 400:
            print(f"  ⚠️ LIMITATION: Only {final_count} clean reviews found.")
        else:
            print(f"  ✅ SUCCESS: {final_count} clean reviews (Meets 400+ target).")
            
        # 5. Save the cleaned dataset as a CSV
        output_path = f'data/raw/{bank_name}_reviews.csv'
        final_df.to_csv(output_path, index=False)
        print(f"  💾 Saved cleanly to {output_path}")
        
    except Exception as e:
        print(f"  ❌ Error processing {bank_name}: {e}")

print("\n--- 🏁 Task 1 Complete! ---")