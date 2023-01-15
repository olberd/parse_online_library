import requests
import logging
import urllib3
from pathlib import Path


urllib3.disable_warnings()

book_url = 'https://tululu.org/txt.php'


def load_book(url, book_file):
    payload = {
        'id': book_file
    }
    response = requests.get(url, params=payload, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    filename = f'id{book_file}.txt'
    path = Path('books', filename)
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open('wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history and response.url == 'https://tululu.org/':
        raise requests.HTTPError


def get_books():
    logging.basicConfig(level=logging.ERROR)
    for book in range(1, 11):
        try:
            load_book(book_url, book)
        except requests.HTTPError:
            logging.error(f'Нет книги с id {book}')
            continue


if __name__ == '__main__':
    get_books()
