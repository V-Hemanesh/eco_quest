import sqlite3

def update_massive_content():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 1. Pollution - Massive Expansion
    pollution_content = """
<div class="briefing-content">
    <h2 class="briefing-title">I. The Comprehensive Science of Pollution</h2>
    <p>Pollution is officially defined as the introduction of harmful materials, known as pollutants, into the natural environment. These pollutants can be natural (like volcanic ash) or human-made (like industrial chemicals). According to the World Health Organization (WHO), pollution is one of the world's greatest environmental risks to health, causing millions of premature deaths globally each year due to cardiovascular and respiratory diseases.</p>

    <h3 class="briefing-section">1. Air Pollution: The Invisible Threat</h3>
    <p>Air pollution is primarily driven by the burning of fossil fuels in vehicles, power plants, and industrial facilities. Key pollutants include:</p>
    <ul>
        <li><strong>Particulate Matter (PM):</strong> Tiny solid or liquid particles suspended in air. PM2.5 can penetrate deep into the lungs and even the bloodstream.</li>
        <li><strong>Carbon Monoxide (CO):</strong> A colorless, odorless gas produced by incomplete combustion, particularly in vehicle engines.</li>
        <li><strong>Nitrogen Oxides (NOx):</strong> Major contributors to smog and acid rain, released from high-temperature combustion.</li>
        <li><strong>CFCs (Chlorofluorocarbons):</strong> Once used in refrigeration, these chemicals are famous for damaging the <strong>Ozone Layer</strong>, which protects Earth from harmful UV radiation. The <strong>Montreal Protocol</strong> is the international treaty that successfully phased out CFCs.</li>
    </ul>
    <p><strong>Photochemical Smog</strong> is a type of air pollution produced when sunlight reacts with nitrogen oxides and volatile organic compounds. Air quality is measured using the <strong>AQI (Air Quality Index)</strong>, where higher values indicate greater health risks.</p>

    <h3 class="briefing-section">2. Water Pollution: Our Lifelines at Risk</h3>
    <p>Water pollution occurs when toxic substances enter water bodies such as lakes, rivers, and oceans. Major sources include untreated sewage and agricultural runoff.</p>
    <ul>
        <li><strong>Eutrophication:</strong> Caused by excess <strong>Nitrogen and Phosphorus</strong> (often from fertilizers), leading to massive algal blooms that deplete oxygen and kill fish.</li>
        <li><strong>Persistent Organic Pollutants (POPs):</strong> Chemicals that do not break down in the environment and <strong>bioaccumulate</strong> in the food web, reaching toxic levels in top predators.</li>
        <li><strong>Ocean Acidification:</strong> Primarily caused by the ocean absorbing excess CO2 from the atmosphere, which lowers the pH and harms coral reefs and shellfish.</li>
    </ul>

    <h3 class="briefing-section">3. Emerging Pollutants</h3>
    <p>Modern pollution also includes <strong>Plastic Pollution</strong>, where plastic objects accumulate in ecosystems, harming wildlife. Additionally, energy itself can be a pollutant: <strong>Thermal Pollution</strong> (excess heat in water), <strong>Light Pollution</strong> (excessive artificial light), and <strong>Noise Pollution</strong> (disruptive sounds that affect animal communication).</p>
</div>
"""

    # 2. Recycling - Massive Expansion
    recycling_content = """
<div class="briefing-content">
    <h2 class="briefing-title">II. Mastering the Circular Economy</h2>
    <p>Recycling is the industrial process of converting waste materials into new products. It is a cornerstone of the <strong>Circular Economy</strong>, which aims to eliminate waste by keeping resources in use for as long as possible.</p>

    <h3 class="briefing-section">1. The Waste Hierarchy</h3>
    <p>The most effective strategy for sustainability is following the Waste Hierarchy:</p>
    <ul>
        <li><strong>Reduce:</strong> The most effective strategy—consuming less to begin with.</li>
        <li><strong>Reuse:</strong> Using an item again for its original purpose without altering its form.</li>
        <li><strong>Recycle:</strong> Processing used materials into new products to reduce the consumption of fresh raw materials.</li>
    </ul>

    <h3 class="briefing-section">2. Material Science in Recycling</h3>
    <p>Different materials have different recycling properties:</p>
    <ul>
        <li><strong>Aluminum:</strong> One of the most efficient materials to recycle. It saves up to <strong>95% of the energy</strong> compared to producing it from its virgin source, a rock called <strong>Bauxite</strong>.</li>
        <li><strong>Plastics:</strong> The most commonly recycled plastic is <strong>PET</strong> (used in water bottles). However, many plastics undergo <strong>Downcycling</strong>, where they are recycled into lower-quality products.</li>
        <li><strong>E-Waste:</strong> Electronics recycling is the primary challenge due to the complex mix of toxic materials and precious metals.</li>
    </ul>

    <h3 class="briefing-section">3. Advanced Waste Management</h3>
    <p><strong>Composting</strong> is the natural process of recycling organic waste (like food scraps) into nutrient-rich soil. <strong>Closed-loop recycling</strong> refers to a process where a product is recycled back into the same product (e.g., a glass bottle becoming a glass bottle). For non-recyclable waste, <strong>Energy Recovery</strong> involves burning trash to generate electricity.</p>
</div>
"""

    # 3. Climate Change - Massive Expansion
    climate_content = """
<div class="briefing-content">
    <h2 class="briefing-title">III. The Climate Emergency: A Global Deep Dive</h2>
    <p><strong>Global Warming</strong> refers to the long-term heating of Earth's climate system, while <strong>Climate Change</strong> includes warming and the "side effects" like melting glaciers and heavier rainstorms. The primary driver of current climate change is human activity, particularly the emission of greenhouse gases.</p>

    <h3 class="brief "section">1. Greenhouse Gas Dynamics</h3>
    <ul>
        <li><strong>Carbon Dioxide (CO2):</strong> Accounts for more than <strong>90% of human-driven emissions</strong>. Forests are vital because they act as <strong>Carbon Sinks</strong>, absorbing CO2 from the air.</li>
        <li><strong>Methane (CH4):</strong> A potent gas that traps significantly more heat than CO2. Major sources include the agriculture industry (livestock) and landfills.</li>
        <li><strong>Global Warming Potential (GWP):</strong> A measure of how much energy the emissions of 1 ton of a gas will absorb over a given period of time, relative to 1 ton of CO2.</li>
    </ul>

    <h3 class="briefing-section">2. Feedback Loops and Effects</h3>
    <p>The <strong>Albedo Effect</strong> is a critical feedback loop: as white ice melts, it exposes dark ocean water, which absorbs more heat, causing more ice to melt. Melting glaciers also lead to <strong>Sea-Level Rise</strong>, threatening coastal cities. The oceans help by absorbing heat, but this leads to <strong>Ocean Acidification</strong>.</p>

    <h3 class="briefing-section">3. The Global Response</h3>
    <p><strong>Mitigation</strong> refers to efforts to reduce or prevent the emission of greenhouse gases. The <strong>Paris Agreement</strong> is a landmark international treaty where nations agreed to limit global temperature increase to well below <strong>2 degrees Celsius</strong>. Individuals can help by reducing their <strong>Carbon Footprint</strong>—the total amount of greenhouse gases generated by our actions.</p>
</div>
"""

    # 4. Water Conservation - Massive Expansion
    water_content = """
<div class="briefing-content">
    <h2 class="briefing-title">IV. Water: The Lifeblood of Sustainability</h2>
    <p>Water is finite. While Earth is covered in water, only approximately <strong>1% is easily accessible freshwater</strong>. Water conservation is also critical for <strong>Energy Conservation</strong>, as moving and treating water requires vast amounts of electricity.</p>

    <h3 class="briefing-section">1. The Giants of Water Usage</h3>
    <p>The <strong>Agriculture Sector</strong> accounts for the majority (about 70%) of global freshwater withdrawals. To improve efficiency, technologies like <strong>Drip Irrigation</strong> are used to deliver water directly to plant roots, minimizing waste.</p>

    <h3 class="briefing-section">2. Groundwater and Coastal Risks</h3>
    <ul>
        <li><strong>Aquifers:</strong> Underground layers of rock that hold water. Over-pumping leads to <strong>Groundwater Depletion</strong>.</li>
        <li><strong>Subsidence:</strong> The sinking of land caused by excessive groundwater extraction.</li>
        <li><strong>Saltwater Intrusion:</strong> In coastal areas, over-pumping can cause seawater to enter freshwater aquifers, making the water undrinkable.</li>
    </ul>

    <h3 class="briefing-section">3. Innovative Solutions</h3>
    <p><strong>Rainwater Harvesting</strong> involves collecting and storing rain for later use. <strong>Greywater</strong> refers to gently used water from sinks and showers that can be reused for irrigation. <strong>Xeriscaping</strong> is a landscaping method that uses native, drought-resistant plants to eliminate the need for supplemental water. <strong>Desalination</strong> (removing salt from seawater) is often seen as a last resort due to its high energy cost and environmental impact.</p>
</div>
"""

    topics_data = [
        (pollution_content, 1),
        (recycling_content, 2),
        (climate_content, 3),
        (water_content, 4)
    ]

    for content, topic_id in topics_data:
        cursor.execute("UPDATE topics SET content = ? WHERE topic_id = ?", (content.strip(), topic_id))

    conn.commit()
    conn.close()
    print("Mission briefings massively expanded with quiz-relevant info!")

if __name__ == "__main__":
    update_massive_content()
