import argparse
import time
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
    if response.url == 'https://tululu.org/':
        raise requests.HTTPError


def download_txt(response, filename, folder='books/'):
    filename = f'{sanitize_filename(filename)}.txt'
    path = Path(folder, filename)
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open('wb') as file:
        file.write(response.content)
    return path


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


def parse_book_page(soup):
    title = soup.find('div', id='content').find('h1').text
    title, author = title.split('::')
    genres_links = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres_links]
    texts = soup.find_all(class_='texts')
    comments = [com.find('span').text for com in texts]
    book_description = {
        'title': title.strip(),
        'author': author.strip(),
        'comments': comments,
        'genres': genres,
    }
    return book_description


def main():
    logging.basicConfig(level=logging.ERROR)
    parser = argparse.ArgumentParser(description='Скачивает файлы с текстами и обложками книг с сайта tululu.org')
    parser.add_argument('start_id', default=1, type=int, help='с какого номера id книги начать загрузку')
    parser.add_argument('end_id', default=10, type=int, help='по какой id книги закончить загрузку')
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id + 1):
        try:
            payload = {'id': book_id}
            response = requests.get(BOOK_TXT_URL, params=payload, verify=False)
            response.raise_for_status()
            check_for_redirect(response)
            book_description_url = f'{BOOK_PAGE_URL}{book_id}'
            book_description_response = requests.get(book_description_url)
            book_description_response.raise_for_status()
            check_for_redirect(book_description_response)
            soup = BeautifulSoup(book_description_response.text, 'lxml')
            book_description = parse_book_page(soup)
            download_txt(response, f'{book_id}. {book_description["title"]}')
            download_image(get_image_url(book_description_url, soup))
            print(book_description)
        except requests.HTTPError:
            logging.error(f'Нет книги с id {book_id}')
            continue
        except requests.ConnectionError:
            logging.error(f'Нет подключения к сайту tululu.org')
            time.sleep(15)
            continue


if __name__ == '__main__':
    main()
