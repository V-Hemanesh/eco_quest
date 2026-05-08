import sqlite3

def update_topics_schema():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 1. Add columns if not exist
    cursor.execute("PRAGMA table_info(topics)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "icon" not in columns:
        cursor.execute("ALTER TABLE topics ADD COLUMN icon TEXT")
    if "description" not in columns:
        cursor.execute("ALTER TABLE topics ADD COLUMN description TEXT")

    # 2. Populate Data
    topics_info = [
        (1, "Pollution", "🏭", "Learn about different types of pollution and how they affect nature."),
        (2, "Recycling", "♻️", "Understand waste management and sustainable reuse."),
        (3, "Climate Change", "🔥", "Explore global warming, greenhouse gases, and solutions."),
        (4, "Water Conservation", "💧", "Learn how to protect and efficiently use water resources."),
        (5, "Biodiversity", "🦁", "Protect the variety of life on Earth."),
        (6, "Renewable Energy", "☀️", "Clean energy sources for a better future."),
        (7, "Sustainable Ag", "🚜", "Farming without harming the planet."),
        (8, "Ocean Conservation", "🐙", "Protect our blue planet and marine life."),
        (9, "Forest Protection", "🌳", "Trees are the lungs of our planet."),
        (10, "Green Cities", "🏢", "Smart and sustainable urban design.")
    ]

    for tid, name, icon, desc in topics_info:
        cursor.execute("""
            UPDATE topics 
            SET icon = ?, description = ? 
            WHERE topic_id = ?
        """, (icon, desc, tid))

    conn.commit()
    conn.close()
    print("Topics table updated with icons and descriptions!")

if __name__ == "__main__":
    update_topics_schema()
