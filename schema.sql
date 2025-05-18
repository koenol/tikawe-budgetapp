CREATE TABLE users {
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
};

CREATE TABLE transactions {
    transaction_id INTEGER PRIMARY KEY,
    amount INTEGER,
    description TEXT,
    date DATE
};