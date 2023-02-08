import argparse
import json
import logging
import time
import requests
from urllib.parse import urljoin, urlsplit, unquote
from bs4 import BeautifulSoup
from utils import check_for_redirect, parse_book_page, download_txt, download_image, get_image_url


TULULU_MAIN_URL = 'https://tululu.org/'
SCIENCE_FICTION_URL = 'https://tululu.org/l55/'
BOOK_TXT_URL = 'https://tululu.org/txt.php'


def fetch_one_page_links(index):
    url = urljoin(SCIENCE_FICTION_URL, str(index))
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    page_url = soup.select('.bookimage > a')
    book_links = [urljoin(TULULU_MAIN_URL, url['href']) for url in page_url]
    return book_links


def fetch_pages_links(start_page=1, end_page=2):
    book_links = []
    for index in range(start_page, end_page):
        book_links.extend(fetch_one_page_links(index))
    return book_links


def main():
    logging.basicConfig(level=logging.ERROR)
    books_descriptions = []

    parser = argparse.ArgumentParser(description='Скачивает файлы с текстами и обложками книг с сайта tululu.org')
    parser.add_argument('--start_page', default=1, type=int, help='с какой страницы начать загрузку')
    parser.add_argument('--end_page', default=701, type=int, help='по какую страницу закончить загрузку')
    args = parser.parse_args()
    book_links = fetch_pages_links(args.start_page, args.end_page)
    for book_link in book_links:
        try:
            book_description_response = requests.get(book_link)
            book_description_response.raise_for_status()
            check_for_redirect(book_description_response)
            soup = BeautifulSoup(book_description_response.text, 'lxml')
            book_description = parse_book_page(soup)
            raw_book_id = unquote(urlsplit(book_link).path)
            book_id = raw_book_id.replace('b', '').replace('/', '')
            payload = {'id': book_id}
            response = requests.get(BOOK_TXT_URL, params=payload, verify=False)
            response.raise_for_status()
            check_for_redirect(response)
            book_path = download_txt(response, f'{book_description["title"]}')
            img_src = download_image(get_image_url(book_link, soup))
            book_description['img_src'] = img_src
            book_description['book_path'] = book_path
            print(book_description)
            books_descriptions.append(book_description)
        except requests.HTTPError:
            logging.error(f'Ошибочная ссылка на книгу')
            continue
        except requests.ConnectionError:
            logging.error(f'Нет подключения к сайту tululu.org')
            time.sleep(15)
            continue
    books_descriptions_json = json.dumps(books_descriptions, ensure_ascii=False)
    with open('books_descriptions.json', 'w', encoding='utf8') as descr_file:
        descr_file.write(books_descriptions_json)


if __name__ == '__main__':
    main()

