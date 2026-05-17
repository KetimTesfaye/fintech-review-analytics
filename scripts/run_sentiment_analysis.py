import pandas as pd
from transformers import pipeline
import os
import glob

# 1. SETUP: Ensure folders exist
os.makedirs('data/processed', exist_ok=True)

# 2. FIND AND MERGE: Grab the bank reviews you already scraped
raw_files = glob.glob('data/raw/*_reviews.csv')

if not raw_files:
    print("❌ Error: I couldn't find your bank files in 'data/raw/'.")
    print("Please make sure CBE_reviews.csv, BOA_reviews.csv, etc., are in that folder.")
else:
    print(f"Found {len(raw_files)} bank files. Merging and cleaning...")
    df_list = [pd.read_csv(f) for f in raw_files]
    df = pd.concat(df_list, ignore_index=True)
    
    # 3. RUN AI MODEL (Task 2): This downloads the DistilBERT model (approx 260MB)
    print("Starting DistilBERT Sentiment Analysis... (This may take a few minutes)")
    classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

    def get_sentiment(text):
        try:
            # I am truncating to 512 characters because that is the model's limit
            result = classifier(str(text)[:512])[0]
            return result['label'], result['score']
        except:
            return "NEUTRAL", 0.0

    # Apply the model to create the missing columns
    results = df['review'].apply(get_sentiment)
    df['sentiment_label'], df['sentiment_score'] = zip(*results)

    # 4. SAVE: Create the file the other scripts are looking for
    output_path = 'data/processed/sentiment_results.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ SUCCESS! Created: {output_path}")
    print("You can now run your aggregation and visualization scripts.")