from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1025",
        database="eco_game"
    )

def get_badge(score, total):
    percentage = (score / total) * 100
    if percentage >= 80:
        return "Eco Hero"
    elif percentage >= 50:
        return "Green Learner"
    else:
        return "Eco Beginner"

def update_progress(user_id, topic_id, score, total):
    conn = get_connection()
    cursor = conn.cursor()

    # Get current level
    current_level = get_user_level(user_id, topic_id)

    # Only level up if passed
    if score >= total // 2:

        if current_level == "Beginner":
            new_level = "Intermediate"
        elif current_level == "Intermediate":
            new_level = "Advanced"
        else:
            new_level = "Advanced"

        # Insert or update
        cursor.execute("""
            INSERT INTO user_progress (user_id, topic_id, level_name)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE level_name=%s
        """, (user_id, topic_id, new_level, new_level))

    conn.commit()
    conn.close()

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")

        conn = get_connection()
        cursor = conn.cursor()

        # 🔐 LOGIN
        if action == "login":
            usn = request.form["usn"]
            password = request.form["password"]

            cursor.execute(
                "SELECT user_id, name FROM users WHERE usn=%s AND password=%s",
                (usn, password)
            )
            user = cursor.fetchone()

            if user:
                session["user_id"] = user[0]
                session["name"] = user[1]
                return redirect("/dashboard")
            else:
                return render_template("login.html", error="Invalid login")

        # 📝 REGISTER
        elif action == "register":
            name = request.form["name"]
            usn = request.form["usn"]
            password = request.form["password"]

            cursor.execute("SELECT * FROM users WHERE usn=%s", (usn,))
            if cursor.fetchone():
                return render_template("login.html", error="User already exists")

            cursor.execute(
                "INSERT INTO users (name, usn, password, total_points, level_name, stars) VALUES (%s,%s,%s,0,'Beginner',0)",
                (name, usn, password)
            )
            conn.commit()

            return render_template("login.html", success="Registered! Please login")

    return render_template("login.html")


def get_user_level(user_id, topic_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT level_name FROM user_progress
        WHERE user_id=%s AND topic_id=%s
    """, (user_id, topic_id))

    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        return "Beginner"
    

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, total_points, level_name, stars
        FROM users WHERE user_id=%s
    """, (session["user_id"],))

    user = cursor.fetchone()

    # Progress % calculation
    xp = user[1]
    progress = (xp % 50) * 2   # 50 XP per level

    return render_template("dashboard.html", user=user, progress=progress)

# LEARNING
@app.route("/learning")
def learning():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT topic_name, content FROM topics")
    topics = cursor.fetchall()

    return render_template("learning.html", topics=topics)

# TOPICS
@app.route("/topics")
def topics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT topic_id, topic_name FROM topics")
    topics = cursor.fetchall()

    return render_template("topics.html", topics=topics)


# QUIZ
from flask import request, render_template, redirect, session

@app.route("/quiz/<int:topic_id>", methods=["GET", "POST"])
def quiz(topic_id):
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

            # 🔹 Update XP + stars
            cursor.execute("""
                UPDATE users
                SET total_points = total_points + %s,
                    stars = stars + %s
                WHERE user_id = %s
            """, (xp_gain, stars_gain, user_id))

            # 🔹 Save level progression
            cursor.execute("""
                INSERT INTO user_progress (user_id, topic_id, level_name)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE level_name=%s
            """, (user_id, topic_id, new_level, new_level))

            conn.commit()

            return render_template(
                "result.html",
                score=score,
                total=total,
                message=message,
                topic_id=topic_id,
                xp_gain=xp_gain,
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
        WHERE topic_id=%s AND difficulty_level=%s
        LIMIT 3
    """, (topic_id, user_level))

    questions = cursor.fetchall()

    return render_template(
        "quiz.html",
        questions=questions,
        level=user_level
    )
# LEADERBOARD
@app.route("/leaderboard")
def leaderboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, total_points, stars
        FROM users ORDER BY total_points DESC
    """)
    data = cursor.fetchall()

    return render_template("leaderboard.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)