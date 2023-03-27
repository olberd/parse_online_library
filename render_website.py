import argparse
import json
import math
import os
import pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


NUM_BOOKS_ON_PAGE = 10


def split_books_by_pages():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', default='./books_descriptions.json', type=pathlib.Path, help='Укажите путь к файлу json')
    args = parser.parse_args()
    with open(args.json_path, 'r', encoding='utf8') as file:
        book_descriptions = json.load(file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('templates/template.html')
    book_descr_chunks = chunked(book_descriptions, NUM_BOOKS_ON_PAGE)
    pages_amount = math.ceil(len(book_descriptions) / NUM_BOOKS_ON_PAGE) + 1
    for idx_page, books_page in enumerate(book_descr_chunks, start=1):
        rendered_page = template.render(
            books_descr=books_page,
            pages_amount=pages_amount,
            current_page=idx_page,
        )
        os.makedirs('pages/', exist_ok=True)
        with open(os.path.join('pages/', f'index{idx_page}.html'), 'w', encoding='utf8') as file:
            file.write(rendered_page)


if __name__ == '__main__':
    split_books_by_pages()
    server = Server()
    server.watch('templates/template.html', split_books_by_pages)
    server.serve(root='.')
