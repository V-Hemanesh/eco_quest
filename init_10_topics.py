import sqlite3

def add_new_topics():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 1. New Topics List
    new_topics = [
        (5, "Biodiversity & Wildlife", "🦁", "Learn about the variety of life on Earth and why protecting it is critical."),
        (6, "Renewable Energy", "☀️", "Explore solar, wind, and other clean energy sources for a better future."),
        (7, "Sustainable Agriculture", "🚜", "Understand how we can grow food without harming the planet."),
        (8, "Ocean Conservation", "🐙", "Protect our blue planet from overfishing and plastic pollution."),
        (9, "Forest Conservation", "🌳", "Trees are the lungs of our planet. Learn how to protect them."),
        (10, "Urban Sustainability", "🏢", "How cities can become green through smart design and transport.")
    ]

    # Insert Topics (if not exist)
    for tid, name, icon, desc in new_topics:
        cursor.execute("SELECT 1 FROM topics WHERE topic_id=?", (tid,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO topics (topic_id, topic_name) VALUES (?, ?)", (tid, name))

    # 2. Add Quizzes for New Topics
    # (topic_id, question, o1, o2, o3, o4, correct, difficulty)
    new_questions = [
        # Biodiversity (5)
        (5, "What does 'biodiversity' refer to?", "Diversity of machines", "Variety of life in an ecosystem", "Different types of weather", "The speed of light", "Variety of life in an ecosystem", "Beginner"),
        (5, "Which of these is a major threat to biodiversity?", "Reforestation", "Habitat destruction", "Clean energy", "Water saving", "Habitat destruction", "Beginner"),
        (5, "What is an 'endangered species'?", "A species that is very common", "A species at risk of extinction", "A species that lives in zoos only", "A new species found", "A species at risk of extinction", "Beginner"),
        
        # Renewable Energy (6)
        (6, "Which of these is a renewable energy source?", "Coal", "Natural Gas", "Solar Energy", "Nuclear Power", "Solar Energy", "Beginner"),
        (6, "What is the main benefit of wind energy?", "It creates noise", "It is infinite and clean", "It uses fossil fuels", "It is expensive", "It is infinite and clean", "Beginner"),
        (6, "What do solar panels convert sunlight into?", "Heat only", "Water", "Electricity", "Sound", "Electricity", "Beginner"),

        # Sustainable Agriculture (7)
        (7, "What is 'organic farming'?", "Farming with machines", "Farming without synthetic chemicals", "Farming in the ocean", "Farming only at night", "Farming without synthetic chemicals", "Beginner"),
        (7, "What is crop rotation?", "Rotating the tractor", "Planting different crops in sequence", "Selling crops in a circle", "Spinning the seeds", "Planting different crops in sequence", "Beginner"),
        (7, "How does composting help agriculture?", "It kills the plants", "It adds nutrients to soil naturally", "It uses more water", "It is a waste of time", "It adds nutrients to soil naturally", "Beginner"),

        # Ocean Conservation (8)
        (8, "What is 'overfishing'?", "Catching fish for food", "Catching fish faster than they can reproduce", "Feeding the fish too much", "Fish jumping out of water", "Catching fish faster than they can reproduce", "Beginner"),
        (8, "Why is plastic dangerous for sea turtles?", "They like to play with it", "They mistake it for food (jellyfish)", "It makes them swim faster", "It is invisible to them", "They mistake it for food (jellyfish)", "Beginner"),
        (8, "What is a Coral Reef often called?", "The desert of the sea", "The rainforest of the sea", "The dark zone", "The silent world", "The rainforest of the sea", "Beginner"),

        # Forest Conservation (9)
        (9, "What is 'deforestation'?", "Planting new trees", "Clearing wide areas of trees", "Painting trees green", "Climbing trees", "Clearing wide areas of trees", "Beginner"),
        (9, "How do forests help combat climate change?", "They make the wind blow", "They absorb Carbon Dioxide", "They reflect all sunlight", "They produce more heat", "They absorb Carbon Dioxide", "Beginner"),
        (9, "Which is a major cause of deforestation?", "Eco-tourism", "Agriculture and logging", "Bird watching", "Hiking", "Agriculture and logging", "Beginner"),

        # Urban Sustainability (10)
        (10, "What is a 'Green Building'?", "A building painted green", "A building designed to be eco-friendly", "A building with no windows", "A building made of paper", "A building designed to be eco-friendly", "Beginner"),
        (10, "Which mode of transport is most sustainable?", "Private SUV", "Electric Public Transport", "Airplane", "Motorcycle", "Electric Public Transport", "Beginner"),
        (10, "What is 'Urban Sprawl'?", "Cities having many parks", "The uncontrolled expansion of urban areas", "Cities getting smaller", "Planting trees in cities", "The uncontrolled expansion of urban areas", "Beginner")
    ]

    for q in new_questions:
        cursor.execute("SELECT 1 FROM questions WHERE question=? AND topic_id=?", (q[1], q[0]))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO questions (topic_id, question, option1, option2, option3, option4, correct_option, difficulty_level) VALUES (?,?,?,?,?,?,?,?)", q)

    # 3. Add Massive Content for New Topics
    # (topic_id, content)
    topic_contents = [
        (5, """
<div class="briefing-content">
    <h2 class="briefing-title">V. Biodiversity: The Web of Life</h2>
    <p>Biodiversity is the variety of all living things and their interactions. It is the foundation of ecosystem services that sustain human life, from food and clean water to medicine and climate regulation.</p>
    <h3 class="briefing-section">1. Why Biodiversity Matters</h3>
    <p>Every species plays a role. If one species disappears, it can cause a "trophic cascade" that disrupts the entire food web. Healthy ecosystems with high biodiversity are more resilient to environmental changes like climate change or disease.</p>
    <h3 class="briefing-section">2. Major Threats</h3>
    <ul>
        <li><strong>Habitat Destruction:</strong> The #1 cause of biodiversity loss, driven by agriculture, mining, and urban sprawl.</li>
        <li><strong>Invasive Species:</strong> Non-native species that disrupt local ecosystems.</li>
        <li><strong>Overexploitation:</strong> Hunting or harvesting species faster than they can recover.</li>
    </ul>
    <h3 class="briefing-section">3. Conservation Strategies</h3>
    <p>Protecting <strong>Endangered Species</strong> involves legal protections, habitat restoration, and creating protected wildlife corridors. <strong>Rewilding</strong> is a strategy of returning areas to their natural state to allow biodiversity to flourish.</p>
</div>
"""),
        (6, """
<div class="briefing-content">
    <h2 class="briefing-title">VI. Renewable Energy: Powering the Future</h2>
    <p>Renewable energy comes from natural sources that replenish themselves faster than they are consumed. Unlike fossil fuels, they produce little to no greenhouse gas emissions.</p>
    <h3 class="briefing-section">1. Solar and Wind Power</h3>
    <ul>
        <li><strong>Solar Energy:</strong> Capturing sunlight using Photovoltaic (PV) cells to create electricity. It's infinite and increasingly affordable.</li>
        <li><strong>Wind Energy:</strong> Using large turbines to convert the kinetic energy of wind into power.</li>
    </ul>
    <h3 class="briefing-section">2. Hydro, Geothermal, and Biomass</h3>
    <p>Other sources include <strong>Hydropower</strong> (energy from moving water), <strong>Geothermal</strong> (heat from within the Earth), and <strong>Biomass</strong> (organic material from plants and animals).</p>
    <h3 class="briefing-section">3. The Energy Transition</h3>
    <p>The goal is to transition away from "Dirty Energy" (coal, oil, gas) to a 100% clean grid. This requires better battery storage and smart grid technology to handle the variable nature of sun and wind.</p>
</div>
"""),
        (7, """
<div class="briefing-content">
    <h2 class="briefing-title">VII. Sustainable Agriculture: Feeding the World Responsibly</h2>
    <p>Current industrial farming uses massive amounts of water and chemicals. Sustainable agriculture seeks to produce food while protecting the soil, water, and climate.</p>
    <h3 class="briefing-section">1. Soil Health and Regenerative Farming</h3>
    <p>Healthy soil is a living ecosystem. <strong>Regenerative Agriculture</strong> focuses on restoring soil organic matter. Techniques include <strong>No-till farming</strong> (not disturbing the soil) and <strong>Cover Cropping</strong>.</p>
    <h3 class="briefing-section">2. Natural Pest Control</h3>
    <p><strong>Organic Farming</strong> avoids synthetic pesticides and fertilizers. Instead, it uses <strong>Crop Rotation</strong> and <strong>Integrated Pest Management (IPM)</strong>—using natural predators like ladybugs to control pests.</p>
    <h3 class="briefing-section">3. Permaculture</h3>
    <p>A design system that mimics natural ecosystems. It emphasizes <strong>Composting</strong> (recycling organic waste into fertilizer) and polycultures (growing many types of plants together).</p>
</div>
"""),
        (8, """
<div class="briefing-content">
    <h2 class="briefing-title">VIII. Ocean Conservation: Protecting the Blue Heart</h2>
    <p>Oceans cover 70% of Earth and produce over half of our oxygen. They are also our largest carbon sink, absorbing 25% of all CO2 emissions.</p>
    <h3 class="briefing-section">1. The Crisis of Plastic</h3>
    <p>Over 8 million tons of plastic enter the ocean every year. Marine animals like <strong>Sea Turtles</strong> often mistake plastic bags for jellyfish, leading to starvation and death. <strong>Microplastics</strong> are now found in every level of the ocean food chain.</p>
    <h3 class="briefing-section">2. Coral Reefs and Marine Life</h3>
    <p>Often called the "Rainforests of the Sea," <strong>Coral Reefs</strong> support 25% of all marine life despite covering only 0.1% of the ocean floor. They are highly sensitive to rising temperatures (Coral Bleaching).</p>
    <h3 class="briefing-section">3. Sustainable Fisheries</h3>
    <p><strong>Overfishing</strong> is a major threat. Creating <strong>Marine Protected Areas (MPAs)</strong> and following sustainable fishing guidelines are essential to allow fish populations to recover.</p>
</div>
"""),
        (9, """
<div class="briefing-content">
    <h2 class="briefing-title">IX. Forest Conservation: The Earth's Lungs</h2>
    <p>Forests are home to 80% of terrestrial biodiversity. They play a critical role in regulating the global climate by sequestering carbon.</p>
    <h3 class="briefing-section">1. The Impact of Deforestation</h3>
    <p><strong>Deforestation</strong> is the permanent removal of trees. It's largely driven by industrial agriculture (cattle, soy, palm oil). When trees are cut down, they release all their stored carbon back into the atmosphere.</p>
    <h3 class="briefing-section">2. Role in Air Quality</h3>
    <p>Trees act as natural air filters, absorbing pollutants like Nitrogen Oxides and Ammonia, and producing the Oxygen we breathe.</p>
    <h3 class="briefing-section">3. Solutions</h3>
    <p><strong>Reforestation</strong> (planting new trees) and <strong>Afforestation</strong> (creating new forests) are key climate solutions. Protecting old-growth forests is even more important, as they store far more carbon than new plantations.</p>
</div>
"""),
        (10, """
<div class="briefing-content">
    <h2 class="briefing-title">X. Urban Sustainability: Green Cities of Tomorrow</h2>
    <p>More than half of the world's population lives in cities. Making urban areas sustainable is key to global environmental health.</p>
    <h3 class="briefing-section">1. Green Infrastructure</h3>
    <p><strong>Green Buildings</strong> are designed to use less energy and water. Features include solar panels, green roofs (plants on top), and natural ventilation.</p>
    <h3 class="briefing-section">2. Sustainable Transport</h3>
    <p>Reducing reliance on cars by investing in <strong>Electric Public Transport</strong>, bike lanes, and walkable neighborhoods. This reduces both air pollution and CO2 emissions.</p>
    <h3 class="briefing-section">3. Reducing Urban Sprawl</h3>
    <p><strong>Urban Sprawl</strong> is the uncontrolled expansion of cities into rural land. Smart city design focuses on high-density, mixed-use development to protect natural habitats around cities.</p>
</div>
""")
    ]

    for tid, content in topic_contents:
        cursor.execute("UPDATE topics SET content = ? WHERE topic_id = ?", (content.strip(), tid))

    conn.commit()
    conn.close()
    print("10 Topics initialized with quizzes and content!")

if __name__ == "__main__":
    add_new_topics()
