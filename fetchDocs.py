from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

url = 'https://www.ishtar-collective.net'

req = Request(f'{url}/categories/book-unveiling', headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()

soup = BeautifulSoup(html_page, 'html.parser')
div = soup.findAll('div', {'class': 'entry-thumbnail col-4'})

links = []
for ele in div:
    links.append(ele.find('a').get('href'))


# print(links)

content = []

for link in links:
    req = Request(url + link, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    descriptions = soup.find('div', {'class': 'description highlightable'})
    print(descriptions)

    paragraphs = descriptions.findAll('p')
    for paragraph in paragraphs:
      content.append(paragraph.text)
        

print(content)