import pandas as pd
import os
import torch
from transformers import pipeline
import spacy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure VADER lexicon is downloaded
nltk.download('vader_lexicon', quiet=True)

# Load Models
print("--- 📦 Loading NLP Models ---")
nlp = spacy.load("en_core_web_sm")
vader = SentimentIntensityAnalyzer()
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def compare_models(text):
    """Briefly compares VADER and DistilBERT for documentation purposes"""
    # VADER
    v_score = vader.polarity_scores(text)['compound']
    
    # DistilBERT
    d_res = sentiment_pipeline(text[:512])[0]
    d_label = d_res['label']
    d_score = d_res['score']
    
    print(f"\n🔍 Comparison for: '{text}'")
    print(f"   VADER Compound Score: {v_score}")
    print(f"   DistilBERT: {d_label} ({d_score:.2f})")

def run_sentiment_analysis(df):
    print("\n--- 🧠 Running Sentiment Analysis (DistilBERT) ---")
    results = []
    texts = df['review'].astype(str).tolist()
    
    for text in texts:
        res = sentiment_pipeline(text[:512])[0]
        results.append(res)
    
    df['sentiment_score'] = [r['score'] for r in results]
    df['sentiment_label_raw'] = [r['label'] for r in results]

    # Confidence Logic for NEUTRAL Classification
    def refine_label(row):
        if row['sentiment_score'] < 0.60:
            return 'NEUTRAL'
        return row['sentiment_label_raw']

    df['sentiment_label'] = df.apply(refine_label, axis=1)
    return df.drop(columns=['sentiment_label_raw'])

# ... (keep your extract_themes and map_theme functions as they were) ...

def main():
    # 1. Load Data
    df = pd.read_csv('data/raw/fintech_reviews_combined.csv') if os.path.exists('data/raw/fintech_reviews_combined.csv') else None
    if df is None: return

    # 2. OPTIONAL: Run Comparison for Rationale Documentation
    sample_text = "The new update is not bad at all, much better than before."
    compare_models(sample_text)

    # 3. Full Pipeline
    df = run_sentiment_analysis(df)
    # ... (rest of your thematic and saving logic) ...
    print("\n✅ Analysis Complete.")

if __name__ == "__main__":
    main()