import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


with open('books_descriptions.json', 'r', encoding='utf8') as file:
    books = json.load(file)


def on_reload():
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
    print('Site rebuilt')


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')




