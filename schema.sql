CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users NOT NULL,
    amount INTEGER NOT NULL DEFAULT 0,
    transaction_type TEXT NOT NULL,
    transaction_message TEXT,
    project_id INTEGER REFERENCES projects NOT NULL,
    date TEXT NOT NULL
);

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT UNIQUE NOT NULL,
    project_owner_id INTEGER REFERENCES users NOT NULL,
    balance INTEGER,
    project_desc TEXT,
    total_transactions INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE project_visibility (
    user_id INTEGER REFERENCES users,
    project_id INTEGER REFERENCES projects,
    view_permission BOOLEAN NOT NULL DEFAULT FALSE,
    edit_permission BOOLEAN NOT NULL DEFAULT FALSE
);