import argparse
import json
import logging
import sys
import time
import requests
from urllib.parse import urljoin, urlsplit, unquote
from bs4 import BeautifulSoup
from parse_tululu_books import check_for_redirect, parse_book_page, download_txt, download_image, get_image_url, \
    TIME_OUT

SCIENCE_FICTION_URL = 'https://tululu.org/l55/'
BOOK_TXT_URL = 'https://tululu.org/txt.php'


def fetch_one_page_links(index):
    url = urljoin(SCIENCE_FICTION_URL, str(index))
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    page_url = soup.select('.bookimage > a')
    book_links = [urljoin(SCIENCE_FICTION_URL, url['href']) for url in page_url]
    return book_links


def fetch_pages_links(start_page=1, end_page=2):
    book_links = []
    for index in range(start_page, end_page):
        try:
            book_links.extend(fetch_one_page_links(index))
        except requests.HTTPError:
            print('Неверная ссылка', file=sys.stderr)
        except requests.ConnectionError:
            print('Нет подключения к интернет', file=sys.stderr)
            time.sleep(TIME_OUT)
    return book_links


def main():
    logging.basicConfig(level=logging.ERROR)
    books_descriptions = []
    parser = argparse.ArgumentParser(description='Скачивает файлы с текстами и обложками книг с сайта tululu.org')
    parser.add_argument('--start_page', default=1, type=int, help='С какой страницы начать загрузку')
    parser.add_argument('--end_page', default=2, type=int, help='По какую страницу закончить загрузку')
    parser.add_argument('--dest_folder', default='books/', type=str,
                        help='Каталог для сохранения текстов, обложек, описания книг')
    parser.add_argument('--skip_imgs', action='store_true', help='Не скачивать обложки')
    parser.add_argument('--skip_txt', action='store_true', help='Не скачивать книги')
    parser.add_argument('--json_path', default='books_descriptions.json', type=str,
                        help='Каталог для файла с описанием книг')
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

            if not args.skip_txt:
                book_path = download_txt(response, f'{book_description["title"]}', args.dest_folder)
                book_description['book_path'] = book_path
            if not args.skip_imgs:
                img_src = download_image(get_image_url(book_link, soup), args.dest_folder)
                book_description['img_src'] = img_src
            print(book_description)
            books_descriptions.append(book_description)
        except requests.HTTPError:
            logging.error(f'Ошибочная ссылка на книгу')
            continue
        except requests.ConnectionError:
            logging.error(f'Нет подключения к сайту tululu.org')
            time.sleep(TIME_OUT)
            continue

    with open(args.json_path, 'w', encoding='utf8') as descr_file:
        json.dump(books_descriptions, descr_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()

