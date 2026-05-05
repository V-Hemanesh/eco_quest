from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
app.secret_key = "secret123"

# =========================
# SAFE DATABASE (NO CRASH)
# =========================
def get_connection():
    try:
        import mysql.connector
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "ecoquest")
        )
    except Exception as e:
        print("DB ERROR:", e)
        return None


# =========================
# BADGE SYSTEM
# =========================
def get_badge(score, total):
    if total == 0:
        return "No Attempt"

    percentage = (score / total) * 100

    if percentage >= 80:
        return "Eco Hero 🏆"
    elif percentage >= 50:
        return "Green Learner 🌱"
    else:
        return "Eco Beginner 🍃"


# =========================
# HOME (FIXES NOT FOUND)
# =========================
@app.route("/")
def home():
    return redirect("/topics")


# =========================
# TOPICS
# =========================
@app.route("/topics")
def topics():
    topics = [
        (1, "Environment"),
        (2, "Recycling"),
        (3, "Climate Change")
    ]
    return render_template("topics.html", topics=topics)


# =========================
# QUIZ
# =========================
@app.route("/quiz/<int:topic_id>", methods=["GET", "POST"])
def quiz(topic_id):

    conn = get_connection()

    # =========================
    # IF DB NOT AVAILABLE (RENDER SAFE MODE)
    # =========================
    if not conn:
        # fallback questions (so app still works)
        questions = [
            ("What is carbon footprint?", "Water use", "Carbon emission", "Oxygen", "Soil", "Carbon emission"),
            ("Main cause of air pollution?", "Trees", "Vehicles", "Rain", "Soil", "Vehicles"),
            ("Noise pollution is caused by?", "Water", "Air", "Noise", "Soil", "Noise")
        ]

        if request.method == "POST":
            score = 0
            total = int(request.form.get("total", 0))

            for i in range(total):
                if request.form.get(f"q{i}") == request.form.get(f"correct{i}"):
                    score += 1

            badge = get_badge(score, total)

            return render_template(
                "result.html",
                score=score,
                total=total,
                badge=badge,
                message="⚠️ Running without database (demo mode)",
                topic_id=topic_id
            )

        return render_template("quiz.html", questions=questions, level="Demo Mode")

    # =========================
    # REAL DB MODE
    # =========================
    cursor = conn.cursor()

    if request.method == "POST":
        score = 0
        total = int(request.form.get("total", 0))

        for i in range(total):
            if request.form.get(f"q{i}") == request.form.get(f"correct{i}"):
                score += 1

        badge = get_badge(score, total)

        return render_template(
            "result.html",
            score=score,
            total=total,
            badge=badge,
            message="Quiz Completed",
            topic_id=topic_id
        )

    cursor.execute("""
        SELECT question, option1, option2, option3, option4, correct_option
        FROM questions
        WHERE topic_id=%s
        LIMIT 3
    """, (topic_id,))

    questions = cursor.fetchall()

    return render_template("quiz.html", questions=questions, level="Live Mode")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))