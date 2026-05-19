import pandas as pd
import os
import spacy
from transformers import pipeline

# 1. SETUP: Load Models
print("--- 📦 Loading NLP Pipeline Models ---")
nlp = spacy.load("en_core_web_sm")
sentiment_model = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# 2. MODULE: Cleaning (Tokenization, Stop-word removal, Lemmatization)
def preprocess_text(text):
    """Handles core NLP cleaning tasks using spaCy."""
    doc = nlp(str(text).lower())
    # Keep nouns, adjectives, and verbs; remove stop words and punctuation
    tokens = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct and token.pos_ in ("NOUN", "ADJ", "VERB")
    ]
    return " ".join(tokens)

# 3. MODULE: Sentiment Analysis
def get_sentiment_data(text):
    """Analyzes sentiment and applies the Neutral threshold."""
    res = sentiment_model(text[:512])[0]
    label, score = res['label'], res['score']
    
    # Apply Neutral logic based on confidence
    final_label = 'NEUTRAL' if score < 0.60 else label
    return final_label, score

# 4. MODULE: Thematic Mapping
def assign_business_theme(clean_text):
    """Maps cleaned keywords to business-relevant issues."""
    themes = {
        "Account Access": ["login", "otp", "password", "access", "sign"],
        "Transaction Performance": ["transfer", "money", "pending", "slow", "fail", "transaction"],
        "UI & Design": ["ui", "interface", "design", "layout", "beautiful", "look"],
        "Customer Support": ["service", "agent", "call", "help", "support", "branch"],
        "System Stability": ["crash", "error", "network", "server", "bug", "update"]
    }
    for theme, keywords in themes.items():
        if any(word in clean_text for word in keywords):
            return theme
    return "General Feedback"

# 5. MAIN EXECUTION PIPELINE
def main():
    input_path = 'data/raw/fintech_reviews_combined.csv'
    output_path = 'data/processed/final_sentiment_results.csv'

    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found.")
        return

    # Load Data
    df = pd.read_csv(input_path)
    print(f"--- ⚙️ Processing {len(df)} reviews ---")

    # Step A: Cleaning/Lemmatization
    df['clean_text'] = df['review'].apply(preprocess_text)

    # Step B: Sentiment Analysis
    # Using zip(*) to unpack the tuple into two separate columns
    sentiment_results = df['review'].apply(get_sentiment_data)
    df['sentiment_label'], df['sentiment_score'] = zip(*sentiment_results)

    # Step C: Thematic Mapping (using the clean text)
    df['identified_theme'] = df['clean_text'].apply(assign_business_theme)

    # Step D: Final Column Formatting (As per Rubric)
    # Required: review_id, review_text, sentiment_label, sentiment_score, identified_theme
    final_df = df[[
        'reviewId', 
        'review', 
        'sentiment_label', 
        'sentiment_score', 
        'identified_theme'
    ]].rename(columns={'reviewId': 'review_id', 'review': 'review_text'})

    # Save
    os.makedirs('data/processed', exist_ok=True)
    final_df.to_csv(output_path, index=False)
    print(f"✅ Pipeline Complete! File saved to: {output_path}")

if __name__ == "__main__":
    main()