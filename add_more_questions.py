import sqlite3

def add_more_questions():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Extra questions for topics 5-10
    extra_questions = [
        # Topic 5: Biodiversity
        (5, "Which biome has the highest biodiversity?", "Tropical Rainforest", "Desert", "Tundra", "Grassland", "Tropical Rainforest", "Beginner"),
        (5, "What is an indicator species?", "A species that reflects the health of an ecosystem", "A species that is newly discovered", "A species that is extinct", "A common pet", "A species that reflects the health of an ecosystem", "Beginner"),
        (5, "What is the primary cause of the current mass extinction?", "Human activities", "Volcanic eruptions", "Asteroid impact", "Solar flares", "Human activities", "Beginner"),
        
        # Topic 6: Renewable Energy
        (6, "Which energy source uses the heat from the Earth's interior?", "Geothermal", "Solar", "Wind", "Biomass", "Geothermal", "Beginner"),
        (6, "What is a 'Smart Grid'?", "An electricity network that uses digital technology", "A grid made of stronger wire", "A grid that only works at night", "A way to trap birds", "An electricity network that uses digital technology", "Beginner"),
        (6, "Which country produces the most wind energy?", "China", "USA", "Germany", "India", "China", "Beginner"),

        # Topic 7: Sustainable Agriculture
        (7, "What is crop rotation?", "Growing different crops in the same area across seasons", "Turning crops upside down", "Moving crops to a different city", "Rotating the seeds before planting", "Growing different crops in the same area across seasons", "Beginner"),
        (7, "What is 'Permaculture'?", "A design system for sustainable living and land use", "A permanent type of fertilizer", "Farming only in the winter", "A type of tractor", "A design system for sustainable living and land use", "Beginner"),
        (7, "What is the benefit of 'No-till' farming?", "It reduces soil erosion", "It makes the soil harder", "It requires more water", "It kills all pests", "It reduces soil erosion", "Beginner"),

        # Topic 8: Ocean Conservation
        (8, "What is 'Ocean Acidification'?", "Decrease in pH caused by CO2 absorption", "The ocean turning into vinegar", "Pollution from car batteries", "Acid rain falling on the sea", "Decrease in pH caused by CO2 absorption", "Beginner"),
        (8, "What are 'Ghost Nets'?", "Abandoned fishing nets that trap marine life", "Nets used by transparent fish", "Nets that only work at night", "Nets made of invisible silk", "Abandoned fishing nets that trap marine life", "Beginner"),
        (8, "Which of these is a 'Marine Protected Area'?", "The Great Barrier Reef", "The Sahara Desert", "Central Park", "Mount Everest", "The Great Barrier Reef", "Beginner"),

        # Topic 9: Forest Protection
        (9, "What is 'Afforestation'?", "Planting trees in an area where there was no forest", "Cutting down old trees", "Burning leaves for fuel", "Counting the number of trees", "Planting trees in an area where there was no forest", "Beginner"),
        (9, "What are the 'Lungs of the Earth'?", "The Amazon Rainforest", "The Arctic Ice Cap", "The Sahara Desert", "The Pacific Ocean", "The Amazon Rainforest", "Beginner"),
        (9, "What is 'Old-Growth Forest'?", "A forest that has attained great age without significant disturbance", "A forest where the trees are sick", "A forest made of stone", "A forest planted last year", "A forest that has attained great age without significant disturbance", "Beginner"),

        # Topic 10: Green Cities
        (10, "What is a 'Green Roof'?", "A roof covered with vegetation", "A roof painted green", "A roof made of recycled money", "A roof that generates solar power only", "A roof covered with vegetation", "Beginner"),
        (10, "What is 'Urban Sprawl'?", "The rapid expansion of the geographic extent of cities", "People stretching in the park", "Buildings falling down", "A type of city cat", "The rapid expansion of the geographic extent of cities", "Beginner"),
        (10, "What is 'Mixed-Use Development'?", "Buildings that combine residential, commercial, and cultural uses", "Using different types of cement", "A park with two benches", "Buildings with both red and blue walls", "Buildings that combine residential, commercial, and cultural uses", "Beginner")
    ]

    cursor.executemany("""
        INSERT INTO questions (topic_id, question, option1, option2, option3, option4, correct_option, difficulty_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, extra_questions)

    conn.commit()
    conn.close()
    print("Added more questions!")

if __name__ == "__main__":
    add_more_questions()
