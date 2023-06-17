CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idimg INTEGER,
    user TEXT,
    title TEXT,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    name TEXT,
    author TEXT,
    path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT,
    email TEXT,
    password TEXT,
    phone TEXT,
    country TEXT,
    city TEXT,
    bio TEXT,
    profile_pic TEXT
);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idimg INTEGER,
    user TEXT,
    vote INTEGER
)