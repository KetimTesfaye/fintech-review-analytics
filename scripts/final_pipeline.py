import pandas as pd
import spacy
import os
from transformers import pipeline

# --- CONFIGURATION ---
INPUT_FILE = 'data/processed/sentiment_results.csv'
OUTPUT_FILE = 'data/processed/final_modular_results.csv'

# Initialize spaCy for NLP (Tokenization & Lemmatization)
# Run 'python -m spacy download en_core_web_sm' if not installed
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# --- MODULE 1: TEXT PREPROCESSING ---
def preprocess_text(text, use_lemmatization=True):
    """Handles tokenization, stop-word removal, and lemmatization."""
    if pd.isna(text): return ""
    
    doc = nlp(str(text).lower())
    
    # Logic: Keep tokens that are not stop words or punctuation
    if use_lemmatization:
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    else:
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        
    return " ".join(tokens)

# --- MODULE 2: THEMATIC MAPPING ---
def get_theme(text):
    """Maps reviews to business-relevant categories."""
    theme_map = {
        'Account Access': ['login', 'otp', 'password', 'sign', 'access', 'fingerprint'],
        'Transaction Performance': ['transfer', 'pay', 'failed', 'slow', 'pending', 'money'],
        'UI & Design': ['interface', 'look', 'design', 'beautiful', 'navigation', 'layout'],
        'Customer Support': ['help', 'call', 'service', 'agent', 'support', 'response'],
        'Feature Requests': ['add', 'feature', 'update', 'missing', 'need']
    }
    text_lower = str(text).lower()
    for theme, keywords in theme_map.items():
        if any(kw in text_lower for kw in keywords):
            return theme
    return 'General Feedback'

# --- MAIN EXECUTION ---
def run_pipeline():
    print("🚀 Starting Modular NLP Pipeline...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found!")
        return

    # Load Data
    df = pd.read_csv(INPUT_FILE)
    
    # 1. Generate Review ID if missing
    if 'review_id' not in df.columns:
        df['review_id'] = range(1, len(df) + 1)

    # 2. NLP Preprocessing (Tokenization & Lemmatization)
    print("🧠 Performing NLP Preprocessing (spaCy)...")
    df['clean_text'] = df['review'].apply(lambda x: preprocess_text(x, use_lemmatization=True))

    # 3. Themes
    print("🏷️ Identifying Themes...")
    df['identified_theme'] = df['review'].apply(get_theme)

    # 4. Final Formatting
    # Selecting the exact columns requested
    final_df = df[[
        'review_id', 
        'review', # review_text
        'sentiment_label', 
        'sentiment_score', 
        'identified_theme'
    ]].rename(columns={'review': 'review_text'})

    # 5. Save Results
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Success! Results saved as '{OUTPUT_FILE}' with {len(final_df)} rows.")

if __name__ == "__main__":
    run_pipeline()