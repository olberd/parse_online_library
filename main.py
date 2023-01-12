import requests
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
    filename = f'id{book_file}.txt'
    path = Path('books', filename)
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open('wb') as file:
        file.write(response.content)


def get_books():
    for book in range(1, 11):
        load_book(book_url, book)


if __name__ == '__main__':
    # load_book(book_url)
    get_books()
