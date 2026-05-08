from jinja2 import Template, Environment

env = Environment(autoescape=True)
html_string = '<h2 style="color: red;">The Guide</h2><p>Pollution is bad.</p>'

t = env.from_string("{{ text | striptags | truncate(120) }}")
print("Result:", t.render(text=html_string))

t2 = env.from_string("{{ text | safe | striptags | truncate(120) }}")
print("Result 2:", t2.render(text=html_string))
