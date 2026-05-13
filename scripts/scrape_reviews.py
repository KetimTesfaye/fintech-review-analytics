import pandas as pd
from google_play_scraper import Sort, reviews
import os

print("--- 🚀 Starting Task 1: Independent Bank Scraper ---")

# Ensure output directory exists
os.makedirs('data/raw', exist_ok=True)

# 🎯 VERIFIED APP IDS
target_apps = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp' 
}

for bank_name, app_id in target_apps.items():
    print(f"\n--- 🏦 Processing {bank_name} ---")
    
    # --- 1. Web Scraping ---
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
                'review text': rev['content'],       
                'rating': rev['score'],              
                'review date': rev['at'],            
                'bank / app name': bank_name,        
                'source': 'Google Play'              
            })
            
        df = pd.DataFrame(bank_data)
        
        # --- 2. Preprocessing ---
        # Clean the data specific to this bank
        df = df.drop_duplicates(subset=['id'])
        df = df.dropna(subset=['review text', 'rating'])
        df['review date'] = pd.to_datetime(df['review date']).dt.strftime('%Y-%m-%d')
        
        # Select final columns (dropping the 'id' column)
        final_df = df[['review text', 'rating', 'review date', 'bank / app name', 'source']]
        
        # --- 3. Validation ---
        final_count = len(final_df)
        if final_count < 400:
            print(f"  ⚠️ LIMITATION: Only {final_count} clean reviews found. (Must document in README)")
        else:
            print(f"  ✅ SUCCESS: {final_count} clean reviews (Meets 400+ target).")
            
        # --- 4. Saving the Data ---
        output_path = f'data/raw/{bank_name}_reviews.csv'
        final_df.to_csv(output_path, index=False)
        print(f"  💾 Saved cleanly to {output_path}")
        
    except Exception as e:
        print(f"  ❌ Error processing {bank_name}: {e}")

print("\n--- 🏁 All 3 banks processed and saved separately! ---")