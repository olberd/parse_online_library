import os.path
import requests
import logging
import urllib3
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


urllib3.disable_warnings()

BOOK_TXT_URL = 'https://tululu.org/txt.php'
BOOK_NAME_URL = 'https://tululu.org/b'


def check_for_redirect(response):
    if response.history and response.url == 'https://tululu.org/':
        raise requests.HTTPError


def parse_title_book(url, book_id):
    book_description_url = f'{url}{book_id}'
    response = requests.get(book_description_url)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('div', id='content').find('h1').text
    title = title.split('::')
    book_name = title[0].strip()
    return book_name


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    filename = f'{sanitize_filename(filename)}.txt'
    path = Path(folder, filename)
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open('wb') as file:
        file.write(response.content)
    return os.path.join(folder, filename)


def main():
    logging.basicConfig(level=logging.ERROR)
    for book_id in range(1, 11):
        payload = {'id': book_id}
        response = requests.get(BOOK_TXT_URL, params=payload, verify=False)
        response.raise_for_status()
        try:
            check_for_redirect(response)
        except requests.HTTPError:
            logging.error(f'Нет книги с id {book_id}')
            continue
        download_txt(response.url, f'{book_id}. {parse_title_book(BOOK_NAME_URL, book_id)}')


if __name__ == '__main__':
    main()
