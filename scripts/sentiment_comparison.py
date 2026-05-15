import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import os

# 1. Load your cleaned reviews
df = pd.read_csv('data/processed/final_thematic_results.csv').head(100) # Testing on 100 for speed

# 2. Initialize Models
vader_analyzer = SentimentIntensityAnalyzer()
transformer_classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

def run_vader(text):
    score = vader_analyzer.polarity_scores(str(text))['compound']
    return 'POSITIVE' if score >= 0.05 else 'NEGATIVE'

def run_transformer(text):
    # Truncate to 512 tokens for DistilBERT
    res = transformer_classifier(str(text)[:512])[0]
    return res['label']

# 3. Process Data
print("Running VADER comparison...")
df['vader_sentiment'] = df['review'].apply(run_vader)

print("Running DistilBERT comparison...")
df['transformer_sentiment'] = df['review'].apply(run_transformer)

# 4. Map User Ratings to Ground Truth for Comparison
# 1-2 stars = NEGATIVE, 4-5 stars = POSITIVE
df['actual_sentiment'] = df['rating'].apply(lambda x: 'POSITIVE' if x >= 4 else ('NEGATIVE' if x <= 2 else 'NEUTRAL'))

# 5. Calculate Accuracy (excluding neutral reviews)
comp_df = df[df['actual_sentiment'] != 'NEUTRAL']
vader_acc = (comp_df['vader_sentiment'] == comp_df['actual_sentiment']).mean()
trans_acc = (comp_df['transformer_sentiment'] == comp_df['actual_sentiment']).mean()

# 6. Visualization
plt.figure(figsize=(10, 5))
models = ['VADER (Lexicon)', 'DistilBERT (Transformer)']
accuracies = [vader_acc, trans_acc]

sns.barplot(x=models, y=accuracies, palette='coolwarm')
plt.ylim(0, 1)
plt.ylabel('Accuracy Score')
plt.title('Sentiment Model Accuracy vs. User Ratings')

# Annotate bars
for i, val in enumerate(accuracies):
    plt.text(i, val + 0.02, f'{val:.1%}', ha='center', fontsize=12, fontweight='bold')

plt.show()