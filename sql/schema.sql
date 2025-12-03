-- schema.sql for bank_reviews database

-- Drop tables if they already exist (safe to rerun)
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

-- Create banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL,
    app_name VARCHAR(255) NOT NULL
);

-- Create reviews table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT NOT NULL REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(50),
    sentiment_score FLOAT,
    source VARCHAR(50)
);

-- Optional: Insert sample banks (so you can link reviews immediately)
INSERT INTO banks (bank_name, app_name) VALUES
('Commercial Bank of Ethiopia', 'CBE Mobile App'),
('Bank of Abyssinia', 'BOA Mobile App'),
('Dashen Bank', 'Dashen Mobile App');