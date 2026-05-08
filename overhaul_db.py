import sqlite3
import os
from datetime import date

def update_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 1. Update users table
    # Check if columns already exist to avoid errors
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "eco_coins" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN eco_coins INTEGER DEFAULT 100")
    if "current_streak" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN current_streak INTEGER DEFAULT 0")
    if "last_active_date" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN last_active_date TEXT")
    if "streak_freeze_active" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN streak_freeze_active INTEGER DEFAULT 0")

    # 2. Create achievements table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        icon TEXT,
        xp_reward INTEGER DEFAULT 50,
        coin_reward INTEGER DEFAULT 20
    )
    """)

    # 3. Create user_achievements table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_achievements (
        user_id INTEGER,
        achievement_id INTEGER,
        date_unlocked TEXT,
        PRIMARY KEY (user_id, achievement_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id)
    )
    """)

    # 4. Create daily_quests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_quests (
        quest_id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        goal_type TEXT, -- 'xp', 'quiz', 'coins'
        goal_value INTEGER,
        coin_reward INTEGER DEFAULT 50
    )
    """)

    # 5. Create user_inventory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_inventory (
        user_id INTEGER,
        item_type TEXT, -- 'heart_refill', 'streak_freeze', 'xp_boost'
        quantity INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, item_type),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # 6. Populate achievements
    achievements = [
        ("Early Bird", "Login for the first time", "🌅", 50, 10),
        ("Knowledge Seeker", "Complete 5 lessons", "📚", 100, 50),
        ("Streak Warrior", "Maintain a 3-day streak", "🔥", 200, 100),
        ("Eco Millionaire", "Earn 1000 Eco-Coins", "💰", 500, 0),
        ("Pollution Pro", "Complete all levels in Pollution", "🏭", 300, 150),
        ("Master Recycler", "Complete all levels in Recycling", "♻️", 300, 150)
    ]
    
    # Use INSERT OR IGNORE if using specific IDs, or check exists
    for ach in achievements:
        cursor.execute("SELECT * FROM achievements WHERE name=?", (ach[0],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO achievements (name, description, icon, xp_reward, coin_reward) VALUES (?,?,?,?,?)", ach)

    # 7. Populate initial quests
    quests = [
        ("Complete 1 Quiz", "quiz", 1, 30),
        ("Earn 50 XP", "xp", 50, 50),
        ("Visit the Shop", "visit", 1, 10)
    ]
    for q in quests:
        cursor.execute("SELECT * FROM daily_quests WHERE description=?", (q[0],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO daily_quests (description, goal_type, goal_value, coin_reward) VALUES (?,?,?,?)", q)

    conn.commit()
    conn.close()
    print("Database overhaul successful!")

if __name__ == "__main__":
    update_database()
