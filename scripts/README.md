Fintech Review Analytics

Task 1: Data Collection & Preprocessing

Scraping Methodology
Data was collected using the `google-play-scraper` Python library. The project targets three major Ethiopian fintech applications:
- CBE (Commercial Bank of Ethiopia)
- BOA (Bank of Abyssinia)
- Dashen (Dashen Bank / Amole)

For each bank, we requested up to 1,000 of the most recent reviews to ensure a robust sample size. The scraper prioritized English language reviews within the Ethiopian (`et`) play store region.

 Date Range
- Start Date:The scraper pulls the newest reviews first (Sort.NEWEST).
- End Date: May 2026 (Current scrape date).
- Format: All dates have been normalized to `YYYY-MM-DD`.

 Preprocessing Steps
To ensure a high-quality dataset, the following cleaning steps were applied automatically:
1. Deduplication:Removed all duplicate reviews based on their unique `reviewId`.
2. Missing Value Handling: Any rows missing the `review` text or the `rating` score were dropped from the final dataset.
3. Column Normalization: Finalized columns are `review`, `rating`, `date`, `bank`, and `source`.

 Limitations Encountered
- Pagination Caps:Google Play Store limits the number of historical reviews retrievable via its public endpoint. While we requested 1,000 per bank, some apps may return fewer depending on their historical visibility.
- Language Filtering: While set to 'en', some reviews may contain Amharic or "Amharic-Latin" (Amharic written in English characters), which will require further NLP processing in later tasks.