# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "secret123"

def get_connection():
    return sqlite3.connect("database.db")

def get_badge(score, total):
    percentage = (score / total) * 100
    if percentage >= 80:
        return "Eco Hero"
    elif percentage >= 50:
        return "Green Learner"
    else:
        return "Eco Beginner"

def update_streak(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT last_active_date, current_streak, streak_freeze_active FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        return
        
    last_date_str, current_streak, streak_freeze = user
    today = date.today()
    today_str = today.isoformat()
    
    if last_date_str:
        last_date = date.fromisoformat(last_date_str)
        delta = (today - last_date).days
        
        if delta == 1:
            # Consecutive day
            cursor.execute("UPDATE users SET current_streak = current_streak + 1, last_active_date = ? WHERE user_id = ?", (today_str, user_id))
        elif delta > 1:
            # Streak broken
            if streak_freeze:
                cursor.execute("UPDATE users SET streak_freeze_active = 0, last_active_date = ? WHERE user_id = ?", (today_str, user_id))
            else:
                cursor.execute("UPDATE users SET current_streak = 1, last_active_date = ? WHERE user_id = ?", (today_str, user_id))
    else:
        # First time
        cursor.execute("UPDATE users SET current_streak = 1, last_active_date = ? WHERE user_id = ?", (today_str, user_id))
        
def update_league(user_id, xp):
    conn = get_connection()
    cursor = conn.cursor()
    
    new_league = 1
    if xp >= 5000: new_league = 5
    elif xp >= 3000: new_league = 4
    elif xp >= 1500: new_league = 3
    elif xp >= 500: new_league = 2
    
    cursor.execute("UPDATE users SET league_id = ? WHERE user_id = ?", (new_league, user_id))
    
    # Mascot Evolution logic
    new_mascot_level = 1
    if xp >= 2000: new_mascot_level = 3
    elif xp >= 500: new_mascot_level = 2
    
    cursor.execute("UPDATE users SET mascot_level = ? WHERE user_id = ?", (new_mascot_level, user_id))
    
    conn.commit()
    conn.close()

def get_notifications(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM notifications WHERE user_id = ? AND is_read = 0", (user_id,))
    notes = [n[0] for n in cursor.fetchall()]
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return notes

def check_achievements(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get user stats
    cursor.execute("SELECT total_points, eco_coins, current_streak FROM users WHERE user_id=?", (user_id,))
    stats = cursor.fetchone()
    xp, coins, streak = stats
    
    # 1. Early Bird
    cursor.execute("SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=1", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO user_achievements (user_id, achievement_id, date_unlocked) VALUES (?, 1, ?)", (user_id, date.today().isoformat()))
        
    # 2. Streak Warrior
    if streak >= 3:
        cursor.execute("SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=3", (user_id,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO user_achievements (user_id, achievement_id, date_unlocked) VALUES (?, 3, ?)", (user_id, date.today().isoformat()))
            
    # 3. Eco Millionaire (simplified to 500 for demo)
    if coins >= 500:
        cursor.execute("SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=4", (user_id,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO user_achievements (user_id, achievement_id, date_unlocked) VALUES (?, 4, ?)", (user_id, date.today().isoformat()))

    conn.commit()
    conn.close()

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/dashboard")
        
    if request.method == "POST":
        action = request.form.get("action")

        conn = get_connection()
        cursor = conn.cursor()

        # 🔐 LOGIN
        if action == "login":
            usn = request.form["usn"]
            password = request.form["password"]

            cursor.execute(
                "SELECT user_id, name FROM users WHERE usn=? AND password=?",
                (usn, password)
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                session["user_id"] = user[0]
                session["name"] = user[1]
                
                # Fetch initial mascot level
                cursor.execute("SELECT mascot_level FROM users WHERE user_id=?", (user[0],))
                m_lvl = cursor.fetchone()[0]
                session["mascot_img"] = "mascot.png"
                if m_lvl == 2: session["mascot_img"] = "mascot_stage2.png"
                elif m_lvl == 3: session["mascot_img"] = "mascot_stage3.png"
                
                return redirect("/dashboard")
            else:
                return render_template("login.html", error="Invalid login")

        # 📝 REGISTER
        elif action == "register":
            name = request.form["name"]
            usn = request.form["usn"]
            password = request.form["password"]

            cursor.execute("SELECT * FROM users WHERE usn=?", (usn,))
            if cursor.fetchone():
                conn.close()
                return render_template("login.html", error="User already exists")

            cursor.execute(
                "INSERT INTO users (name, usn, password, total_points, level_name, stars) VALUES (?,?,?,0,'Beginner',0)",
                (name, usn, password)
            )
            conn.commit()
            conn.close()

            return render_template("login.html", success="Registered! Please login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def require_login():
    if "user_id" not in session:
        return redirect("/")
    
def get_user_level(user_id, topic_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT level_name FROM user_progress
        WHERE user_id=? AND topic_id=?
    """, (user_id, topic_id))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return "Beginner"
    

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    update_streak(user_id)
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.name, u.total_points, u.level_name, u.stars, u.eco_coins, u.current_streak, u.mascot_level, l.name, l.icon
        FROM users u 
        JOIN leagues l ON u.league_id = l.league_id
        WHERE u.user_id=?
    """, (user_id,))
    user_row = cursor.fetchone()
    
    update_league(user_id, user_row[1])
    check_achievements(user_id)
    notifications = get_notifications(user_id)

    # Fetch Achievements
    cursor.execute("""
        SELECT a.name, a.icon, a.description 
        FROM achievements a
        JOIN user_achievements ua ON a.achievement_id = ua.achievement_id
        WHERE ua.user_id = ?
        LIMIT 3
    """, (user_id,))
    achievements = cursor.fetchall()

    # Fetch Daily Quests
    cursor.execute("SELECT description, coin_reward FROM daily_quests LIMIT 3")
    quests = cursor.fetchall()
    
    conn.close()

    # Progress % calculation
    xp = user_row[1]
    progress = (xp % 50) * 2   # 50 XP per level
    rank = "Seedling"
    if xp > 500: rank = "Oak"
    elif xp > 200: rank = "Sapling"
    elif xp > 100: rank = "Sprout"

    # Pass mascot image path based on level
    mascot_img = "mascot.png"
    if user_row[6] == 2: mascot_img = "mascot_stage2.png"
    elif user_row[6] == 3: mascot_img = "mascot_stage3.png"
    session["mascot_img"] = mascot_img

    return render_template("dashboard.html", 
                         user=user_row, 
                         progress=progress, 
                         rank=rank,
                         achievements=achievements,
                         quests=quests,
                         notifications=notifications,
                         mascot_img=mascot_img,
                         league_name=user_row[7],
                         league_icon=user_row[8])

# LEARNING
@app.route("/learning")
def learning():
    if "user_id" not in session:
        return redirect("/")
        
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT topic_id, topic_name, content FROM topics")
    topics = cursor.fetchall()
    conn.close()

    return render_template("learning.html", topics=topics)

@app.route("/learning/<int:topic_id>")
def topic_detail(topic_id):
    if "user_id" not in session:
        return redirect("/")
        
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT topic_id, topic_name, content FROM topics WHERE topic_id=?", (topic_id,))
    topic = cursor.fetchone()
    conn.close()

    if not topic:
        return redirect("/learning")

    return render_template("topic_detail.html", topic=topic)

# TOPICS
# TOPICS / MISSION ZONE
@app.route("/topics")
def topics():
    check = require_login()
    if check:
        return check

    user_id = session["user_id"]
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic_id, topic_name, icon, description FROM topics")
    rows = cursor.fetchall()
    conn.close()

    topics_data = []
    for row in rows:
        topics_data.append({
            "id": row[0],
            "name": row[1],
            "icon": row[2],
            "desc": row[3],
            "difficulty": get_user_level(user_id, row[0])
        })

    return render_template("topics.html", topics=topics_data)


# QUIZ
from flask import request, render_template, redirect, session

@app.route("/quiz/<int:topic_id>", methods=["GET", "POST"])
def quiz(topic_id):
    if "user_id" not in session:
        return redirect("/")
        
    conn = get_connection()
    cursor = conn.cursor()

    user_id = session["user_id"]

    # 🔹 Get current level
    user_level = get_user_level(user_id, topic_id)

    # ======================
    # POST (Submit quiz)
    # ======================
    if request.method == "POST":
        score = 0
        total = int(request.form.get("total", 0))

        # Calculate score
        for i in range(total):
            if request.form.get(f"q{i}") == request.form.get(f"correct{i}"):
                score += 1

        xp_gain = score * 10
        stars_gain = score

        # ======================
        # PASS CONDITION
        # ======================
        if score >= total // 2:

            if user_level == "Beginner":
                new_level = "Intermediate"
                message = "🎉 Level Up! Beginner → Intermediate"

            elif user_level == "Intermediate":
                new_level = "Advanced"
                message = "🔥 Level Up! Intermediate → Advanced"

            else:
                # Already max level
                message = "🏆 Topic Completed!"

                return render_template(
                    "result.html",
                    score=score,
                    total=total,
                    message=message,
                    topic_id=topic_id,
                    xp_gain=xp_gain,
                    is_pass=True
                )

            coin_gain = score * 5
            
            # 🔹 Update XP + stars + coins
            cursor.execute("""
                UPDATE users
                SET total_points = total_points + ?,
                    stars = stars + ?,
                    eco_coins = eco_coins + ?
                WHERE user_id = ?
            """, (xp_gain, stars_gain, coin_gain, user_id))

            # 🔹 Save level progression
            cursor.execute("""
                INSERT OR REPLACE INTO user_progress (user_id, topic_id, level_name)
                VALUES (?, ?, ?)
            """, (user_id, topic_id, new_level))

            conn.commit()
            conn.close()
            
            check_achievements(user_id)

            return render_template(
                "result.html",
                score=score,
                total=total,
                message=message,
                topic_id=topic_id,
                xp_gain=xp_gain,
                coin_gain=coin_gain,
                is_pass=True
            )

        # ======================
        # FAIL CONDITION
        # ======================
        else:
            return render_template(
                "result.html",
                score=score,
                total=total,
                message="❌ Try again to unlock next level",
                topic_id=topic_id,
                xp_gain=0,
                is_pass=False
            )

    # ======================
    # GET (Load quiz)
    # ======================
    cursor.execute("""
        SELECT question, option1, option2, option3, option4, correct_option
        FROM questions
        WHERE topic_id=? AND difficulty_level=?
        ORDER BY RANDOM()
        LIMIT 3
    """, (topic_id, user_level))

    questions = cursor.fetchall()
    conn.close()

    return render_template(
        "quiz.html",
        questions=questions,
        level=user_level
    )
# SHOP
@app.route("/shop")
def shop():
    if "user_id" not in session: return redirect("/")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT eco_coins FROM users WHERE user_id=?", (session["user_id"],))
    coins = cursor.fetchone()[0]
    
    cursor.execute("SELECT item_type, quantity FROM user_inventory WHERE user_id=?", (session["user_id"],))
    inventory = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    
    items = [
        {"id": "heart_refill", "name": "Heart Refill", "price": 50, "icon": "❤️", "desc": "Instantly restores all lives."},
        {"id": "streak_freeze", "name": "Streak Freeze", "price": 200, "icon": "❄️", "desc": "Keep your streak even if you miss a day."},
        {"id": "xp_boost", "name": "XP Boost", "price": 150, "icon": "⚡", "desc": "Double XP for your next quiz."}
    ]
    
    return render_template("shop.html", coins=coins, items=items, inventory=inventory)

@app.route("/buy/<item_id>")
def buy_item(item_id):
    if "user_id" not in session: return redirect("/")
    user_id = session["user_id"]
    
    prices = {"heart_refill": 50, "streak_freeze": 200, "xp_boost": 150}
    if item_id not in prices: return redirect("/shop")
    
    price = prices[item_id]
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT eco_coins FROM users WHERE user_id=?", (user_id,))
    coins = cursor.fetchone()[0]
    
    if coins >= price:
        # Deduct coins
        cursor.execute("UPDATE users SET eco_coins = eco_coins - ? WHERE user_id = ?", (price, user_id))
        
        # Add to inventory
        cursor.execute("""
            INSERT INTO user_inventory (user_id, item_type, quantity)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, item_type) DO UPDATE SET quantity = quantity + 1
        """, (user_id, item_id))
        
        # Special case: Streak Freeze
        if item_id == "streak_freeze":
            cursor.execute("UPDATE users SET streak_freeze_active = 1 WHERE user_id = ?", (user_id,))
            
        conn.commit()
    
    conn.close()
    return redirect("/shop")

# LEADERBOARD
@app.route("/leaderboard")
def leaderboard():
    if "user_id" not in session:
        return redirect("/")
        
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, total_points, stars
        FROM users ORDER BY total_points DESC
    """)
    data = cursor.fetchall()
    conn.close()

    return render_template("leaderboard.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)