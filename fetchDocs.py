from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from langchain_core.documents import Document


url = 'https://www.ishtar-collective.net'


def fetch_docs():
    req = Request(f'{url}/categories/book-unveiling',
                  headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    div = soup.findAll('div', {'class': 'entry-thumbnail col-4'})

    links = []
    for ele in div:
        links.append(ele.find('a').get('href'))

    # print(links)

    docs = []

    for link in links:
        req = Request(url + link, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()

        soup = BeautifulSoup(html_page, 'html.parser')
        descriptions = soup.find('div', {'class': 'description highlightable'})
        # print(descriptions)

        paragraphs = descriptions.findAll('p')

        metadata = {
            "source": re.search(r"\/entries\/([A-Za-z0-9\S]+)#book-unveiling", link).group(1)
        }

        for paragraph in paragraphs:
            docs.append(
                Document(page_content=paragraph.text, metadata=metadata))

    # print(docs)
    return docs
