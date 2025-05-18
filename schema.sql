CREATE TABLE users {
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
};

CREATE TABLE transaction {
    transaction_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER,
    transaction_type TEXT,
    transaction_message TEXT,
    date DATE
};  

CREATE TABLE balance {
    user_id INTEGER,
    balance INTEGER,
    total_transactions INTEGER
};