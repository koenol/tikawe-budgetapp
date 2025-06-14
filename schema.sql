CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users,
    amount INTEGER,
    transaction_type TEXT,
    transaction_message TEXT,
    project_id INTEGER REFERENCES projects,
    date TEXT
); 

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    project_owner_id INTEGER REFERENCES users,
    balance INTEGER,
    total_transactions INTEGER
);

CREATE TABLE project_visibility (
    user_id INTEGER REFERENCES users,
    project_id INTEGER REFERENCES projects,
    view_permission BOOLEAN,
    edit_permission BOOLEAN
);

