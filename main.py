import os.path
from urllib.parse import urljoin, unquote, urlsplit
import requests
import logging
import urllib3
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


urllib3.disable_warnings()

BOOK_TXT_URL = 'https://tululu.org/txt.php'
BOOK_PAGE_URL = 'https://tululu.org/b'


def check_for_redirect(response):
    if response.history and response.url == 'https://tululu.org/':
        raise requests.HTTPError


def get_book_page_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def parse_title_book(soup):
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


def get_image_url(book_description_url, soup):
    image_url = soup.find('div', class_='bookimage').find('img')['src']
    full_image_url = urljoin(book_description_url, image_url)
    return full_image_url


def download_image(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    filename = unquote(urlsplit(url).path)
    filename = filename.split('/')[-1]
    path = Path(folder, filename)
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open('wb') as file:
        file.write(response.content)


def download_comments(soup):
    texts = soup.find_all(class_='texts')
    comments = []
    for com in texts:
        comment = com.find('span').text
        comments.append(comment)
    return comments


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
        book_description_url = f'{BOOK_PAGE_URL}{book_id}'
        book_description_response = requests.get(book_description_url)
        response.raise_for_status()
        soup = BeautifulSoup(book_description_response.text, 'lxml')

        download_txt(response.url, f'{book_id}. {parse_title_book(soup)}')
        download_image(get_image_url(book_description_url, soup))
        print(parse_title_book(soup))
        print(download_comments(soup))


if __name__ == '__main__':
    main()
