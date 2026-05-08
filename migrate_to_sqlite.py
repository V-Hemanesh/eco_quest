import mysql.connector
import sqlite3
import os

# 1. Connect to MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1025",
    database="eco_game"
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

# 2. Connect to SQLite
sqlite_db = "database.db"
if os.path.exists(sqlite_db):
    os.remove(sqlite_db)
sqlite_conn = sqlite3.connect(sqlite_db)
sqlite_cursor = sqlite_conn.cursor()

# 3. Create Tables in SQLite
sqlite_cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    usn TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    total_points INTEGER DEFAULT 0,
    level_name TEXT DEFAULT 'Beginner',
    stars INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS topics (
    topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT NOT NULL,
    content TEXT
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER,
    question TEXT NOT NULL,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_option TEXT,
    difficulty_level TEXT,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);

CREATE TABLE IF NOT EXISTS user_progress (
    user_id INTEGER,
    topic_id INTEGER,
    level_name TEXT,
    PRIMARY KEY (user_id, topic_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);
""")

# 4. Migrate Users
mysql_cursor.execute("SELECT * FROM users")
for row in mysql_cursor.fetchall():
    sqlite_cursor.execute(
        "INSERT INTO users (user_id, name, usn, password, total_points, level_name, stars) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (row['user_id'], row['name'], row['usn'], row['password'], row['total_points'], row['level_name'], row['stars'])
    )

# 5. Migrate Topics
mysql_cursor.execute("SELECT * FROM topics")
for row in mysql_cursor.fetchall():
    sqlite_cursor.execute(
        "INSERT INTO topics (topic_id, topic_name, content) VALUES (?, ?, ?)",
        (row['topic_id'], row['topic_name'], row['content'])
    )

# 6. Migrate Questions
mysql_cursor.execute("SELECT * FROM questions")
for row in mysql_cursor.fetchall():
    sqlite_cursor.execute(
        "INSERT INTO questions (topic_id, question, option1, option2, option3, option4, correct_option, difficulty_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (row['topic_id'], row['question'], row['option1'], row['option2'], row['option3'], row['option4'], row['correct_option'], row['difficulty_level'])
    )

# 7. Migrate Progress
mysql_cursor.execute("SELECT * FROM user_progress")
for row in mysql_cursor.fetchall():
    sqlite_cursor.execute(
        "INSERT INTO user_progress (user_id, topic_id, level_name) VALUES (?, ?, ?)",
        (row['user_id'], row['topic_id'], row['level_name'])
    )

sqlite_conn.commit()
mysql_conn.close()
sqlite_conn.close()
print("Migration to SQLite complete! 'database.db' created.")
