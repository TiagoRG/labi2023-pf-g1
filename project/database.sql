CREATE TABLE comments (
    id AUTOINCREMENT PRIMARY KEY,
    idimg INTEGER,
    user TEXT,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE images (
    id AUTOINCREMENT PRIMARY KEY,
    name TEXT,
    author TEXT,
    path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id AUTOINCREMENT PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    password TEXT
);

CREATE TABLE votes (
    id AUTOINCREMENT PRIMARY KEY,
    idimg INTEGER,
    ups INTEGER,
    downs INTEGER
)