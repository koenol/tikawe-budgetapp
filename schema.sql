CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users,
    amount INTEGER NOT NULL DEFAULT 0,
    transaction_type TEXT NOT NULL,
    transaction_message TEXT,
    project_id INTEGER REFERENCES projects,
    date TEXT NOT NULL
);

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_owner_id INTEGER REFERENCES users,
    balance INTEGER NOT NULL DEFAULT 0,
    total_transactions INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE project_visibility (
    user_id INTEGER REFERENCES users,
    project_id INTEGER REFERENCES projects,
    view_permission BOOLEAN NOT NULL DEFAULT FALSE,
    edit_permission BOOLEAN NOT NULL DEFAULT FALSE
);

