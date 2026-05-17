import pandas as pd
import os

# 1. Path to your combined sentiment results
input_path = 'data/processed/sentiment_results.csv'

if not os.path.exists(input_path):
    print(f"❌ Error: {input_path} not found.")
else:
    # 2. Load the data
    df = pd.read_csv(input_path)
    
    # 3. Perform the aggregation (Mean Sentiment Score)
    agg_table = df.groupby(['bank', 'rating'])['sentiment_score'].mean().unstack()

    # 4. RENAME COLUMNS: Add the "-star" suffix to the headers
    agg_table.columns = [f"{int(col)}-star" for col in agg_table.columns]

    # 5. Round results for professional look
    agg_table = agg_table.round(4)

    # 6. Display the final table
    print("\n" + "="*70)
    print("MEAN SENTIMENT CONFIDENCE BY BANK & RATING")
    print("="*70)
    print(agg_table)

    # 7. Save the final formatted table
    output_path = 'data/processed/final_formatted_sentiment_table.csv'
    agg_table.to_csv(output_path)
    print(f"\n✅ Professional table saved to: {output_path}")