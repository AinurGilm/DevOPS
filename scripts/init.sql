CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    features JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    probability JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
