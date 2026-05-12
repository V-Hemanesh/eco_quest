import sqlite3

def extreme_db_overhaul():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 1. Update users table for mascot evolution and leagues
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "mascot_level" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN mascot_level INTEGER DEFAULT 1")
    if "league_id" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN league_id INTEGER DEFAULT 1") # 1=Bronze, 2=Silver, etc.
    if "max_combo" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN max_combo INTEGER DEFAULT 0")

    # 2. Create leagues table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leagues (
        league_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        min_xp INTEGER,
        icon TEXT
    )
    """)
    
    leagues = [
        (1, "Bronze League", 0, "🥉"),
        (2, "Silver League", 500, "🥈"),
        (3, "Gold League", 1500, "🥇"),
        (4, "Emerald League", 3000, "💎"),
        (5, "Titan League", 5000, "👑")
    ]
    for l in leagues:
        cursor.execute("INSERT OR REPLACE INTO leagues VALUES (?,?,?,?)", l)

    # 3. Create social notifications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        is_read INTEGER DEFAULT 0,
        date_sent TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Extreme Database Overhaul Complete!")

if __name__ == "__main__":
    extreme_db_overhaul()
