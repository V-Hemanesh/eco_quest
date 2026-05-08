from jinja2 import Template

html_string = '<h2 style="color: var(--primary-dark);">The Guide</h2><p>Pollution is bad.</p>'

t1 = Template("{{ text | striptags | truncate(120) }}")
print("T1:", t1.render(text=html_string))

t2 = Template("{{ text | safe | striptags | truncate(120) }}")
print("T2:", t2.render(text=html_string))

