CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER,
    transaction_type TEXT,
    transaction_message TEXT,
    project_id INTEGER,
    date TEXT
); 

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY
    project_owner_id INTEGER,
    balance INTEGER,
    total_transactions INTEGER
);

CREATE TABLE project_visibility (
    user_id INTEGER,
    project_id INTEGER,
    view_permission BOOLEAN,
    edit_permission BOOLEAN
);

