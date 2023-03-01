import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

with open('books_descriptions.json', 'r', encoding='utf8') as file:
    books = json.load(file)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')


rendered_page = template.render(
    books=books,
)

with open('index.html', 'w', encoding='utf8') as file:
    file.write(rendered_page)

