import pandas as pd
import os

# 1. Load your results
input_path = 'data/processed/sentiment_results.csv'

if not os.path.exists(input_path):
    print("❌ sentiment_results.csv not found! Run your sentiment script first.")
else:
    df = pd.read_csv(input_path)

    # 2. Define the Keywords for each Theme
    theme_keywords = {
        'Account Access': ['login', 'otp', 'password', 'sign', 'access', 'lock', 'fingerprint'],
        'Transaction Performance': ['transfer', 'pay', 'failed', 'slow', 'pending', 'money', 'transaction'],
        'UI & Design': ['interface', 'look', 'design', 'beautiful', 'navigation', 'color', 'layout'],
        'Customer Support': ['help', 'call', 'service', 'agent', 'support', 'response', 'contact'],
        'Feature Requests': ['add', 'feature', 'update', 'missing', 'need', 'bill', 'statement']
    }

    def identify_theme(text):
        text = str(text).lower()
        for theme, keywords in theme_keywords.items():
            if any(kw in text for kw in keywords):
                return theme
        return 'General Feedback'

    # 3. Apply the mapping
    df['theme'] = df['review'].apply(identify_theme)

    # 4. Create the Summary Table (Count of complaints/compliments per theme)
    theme_summary = df.groupby(['bank', 'theme']).size().unstack(fill_value=0)

    print("\n" + "="*60)
    print("THEMATIC DISTRIBUTION PER BANK")
    print("="*60)
    print(theme_summary)

    # 5. Save the enriched data
    df.to_csv('data/processed/final_thematic_results.csv', index=False)
    theme_summary.to_csv('data/processed/theme_distribution.csv')
    print("\n✅ Thematic results saved to data/processed/final_thematic_results.csv")