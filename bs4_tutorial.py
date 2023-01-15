import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('main').find('header').find('h1')
image = soup.find('img', class_='attachment-post-image')['src']
content = soup.find('div', class_='entry-content')
print(title_tag.text, image)
print(content.text)
