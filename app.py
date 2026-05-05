from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"


# =========================
# DATABASE CONNECTION (SAFE)
# =========================
def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",   # ⚠️ will replace with cloud DB later
            user="root",
            password="",
            database="ecoquest"
        )
    except:
        return None


# =========================
# HOME ROUTE (FIXES NOT FOUND)
# =========================
@app.route("/")
def home():
    return redirect("/topics")


# =========================
# GET USER LEVEL
# =========================
def get_user_level(user_id, topic_id):
    conn = get_connection()
    if not conn:
        return "Beginner"

    cursor = conn.cursor()
    cursor.execute("""
        SELECT level_name FROM user_progress
        WHERE user_id=%s AND topic_id=%s
    """, (user_id, topic_id))

    result = cursor.fetchone()
    return result[0] if result else "Beginner"


# =========================
# TOPICS PAGE
# =========================
@app.route("/topics")
def topics():
    # temporary topics (can replace with DB later)
    topics = [
        (1, "Environment"),
        (2, "Recycling"),
        (3, "Climate Change")
    ]
    return render_template("topics.html", topics=topics)


# =========================
# QUIZ ROUTE
# =========================
@app.route("/quiz/<int:topic_id>", methods=["GET", "POST"])
def quiz(topic_id):

    # ⚠️ TEMP USER (replace with login system later)
    user_id = 1

    conn = get_connection()

    # =========================
    # HANDLE DB FAILURE (IMPORTANT FOR RENDER)
    # =========================
    if not conn:
        return "⚠️ Database not connected (use cloud DB)"

    cursor = conn.cursor()

    user_level = get_user_level(user_id, topic_id)

    # =========================
    # POST (SUBMIT QUIZ)
    # =========================
    if request.method == "POST":
        score = 0
        total = int(request.form.get("total", 0))

        for i in range(total):
            if request.form.get(f"q{i}") == request.form.get(f"correct{i}"):
                score += 1

        xp_gain = score * 10
        stars_gain = score

        # PASS CONDITION
        if score >= total // 2:

            if user_level == "Beginner":
                new_level = "Intermediate"
                message = "🎉 Level Up! Beginner → Intermediate"

            elif user_level == "Intermediate":
                new_level = "Advanced"
                message = "🔥 Level Up! Intermediate → Advanced"

            else:
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

            # UPDATE XP + STARS
            cursor.execute("""
                UPDATE users
                SET total_points = total_points + %s,
                    stars = stars + %s
                WHERE user_id = %s
            """, (xp_gain, stars_gain, user_id))

            # SAVE LEVEL
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

        # FAIL
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

    # =========================
    # GET (LOAD QUESTIONS)
    # =========================
    cursor.execute("""
        SELECT question, option1, option2, option3, option4, correct_option
        FROM questions
        WHERE topic_id=%s AND difficulty_level=%s
        LIMIT 3
    """, (topic_id, user_level))

    questions = cursor.fetchall()

    return render_template("quiz.html", questions=questions, level=user_level)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))