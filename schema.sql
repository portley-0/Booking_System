DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS bookings;

CREATE TABLE bookings
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    booking TEXT NOT NULL,
    date TEXT NOT NULL
);
