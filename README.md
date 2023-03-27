# Парсер книг с сайта tululu.org  

Скрипт загружает книги с сайта [tululu.org](https://tululu.org/). 

Загруженные книги отображаются на сайте по адресу: 
https://olberd.github.io/parse_online_library/pages/index1.html

### Как установить  

- Python3 должен быть установлен.
- Создайте виртуальное окружение (необязательно)

Для Linux
```
python -m venv .venv
source .venv/bin/activate
```
Для Windows
```
python -m venv venv
venv\Scripts\activate
```
- Установите зависимости командой 
```
pip install -r requirements.txt
```

### Инструкции по использованию.
#### parse_tululu_books.py
```
python parse_tululu_books.py [-h] [--start_id] [--end_id]
```
Аргументы:

`-h, --help` выводит справочную информацию
`--start_page` индекс книги начала загрузки  
`--end_page` индекс книги по который закончить загрузку.
Без аргументов скрипт скачивает книги с 1 по 10 индекс.


Например:
```
python3 parse_tululu_books.py 10 20
```
Книги будут загружены в папку `books` в каталоге запуска скрипта, обложки в папку `images`.
В консоль будут выводиться названия книг, авторы, жанры.

#### parse_tululu_category.py

```
parse_tululu_category.py [-h] [--start_page] [--end_page] [--dest_folder] [--json_path] [--skip_imgs] [--skip_txt]
```
Аргументы:  
`-h, --help` выводит справочную информацию  
`--start_page` с какой страницы начать загрузку  
`--end_page` по какую страницу закончить загрузку  
`--dest_folder` Каталог для сохранения текстов, обложек, описания книг (по умолчанию "books/")   
`--json_path` Каталог для файла с описанием книг  
`--skip_imgs` Не скачивать обложки  
`--skip_txt` Не скачивать книги

### Как запустить локальную онлайн-библиотеку
Запустить сервер 
```
python render_website.py
```
Перейти по адресу 

http://127.0.0.1:5500/pages/index1.html

### Как запустить оффлайн-библиотеку
Открыть любой файл со страницей в каталоге `pages`, например `index1.html`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).