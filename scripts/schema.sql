-- Clear existing tables if they exist to allow clean script re-runs
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

-- 1. Create Banks Table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(50) UNIQUE NOT NULL,
    app_name VARCHAR(150) NOT NULL
);

-- 2. Create Reviews Table with strict constraints
CREATE TABLE reviews (
    review_id INT PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20) NOT NULL CHECK (sentiment_label IN ('POSITIVE', 'NEGATIVE', 'NEUTRAL')),
    sentiment_score NUMERIC(5,4) NOT NULL,
    identified_theme VARCHAR(50) NOT NULL,
    source VARCHAR(50) DEFAULT 'Google Play'
);