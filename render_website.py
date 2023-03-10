import json
import math
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


NUM_BOOKS_ON_PAGE = 10

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
    pages_amount = math.ceil(len(books) / NUM_BOOKS_ON_PAGE) + 1
    for idx_page, books_page in enumerate(books_chunk, start=1):
        rendered_page = template.render(
            books=books_page,
            pages_amount=pages_amount,
            current_page=idx_page,
        )

        with open(os.path.join('pages/', f'index{idx_page}.html'), 'w', encoding='utf8') as file:
            file.write(rendered_page)


def on_reload():
    split_books_by_pages()

    print('Site rebuilt')


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
# server.serve(root='.', default_filename='pages/index1.html')




