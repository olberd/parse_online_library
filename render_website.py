import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


NUM_BOOKS_ON_PAGE = 20

with open('books_descriptions.json', 'r', encoding='utf8') as file:
    books = json.load(file)


def split_books_by_pages():
    os.makedirs('pages/', exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    books_chunk = chunked(books, NUM_BOOKS_ON_PAGE)
    for id, books_page in enumerate(books_chunk, 1):
        rendered_page = template.render(
            books=books_page,
        )

        with open(os.path.join('pages/', f'index{id}.html'), 'w', encoding='utf8') as file:
            file.write(rendered_page)


split_books_by_pages()


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


# on_reload()
# server = Server()
# server.watch('template.html', on_reload)
# server.serve(root='.')




