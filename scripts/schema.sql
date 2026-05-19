CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(255) PRIMARY KEY, 
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    identified_theme VARCHAR(100),
    source VARCHAR(50) DEFAULT 'Google Play'
);