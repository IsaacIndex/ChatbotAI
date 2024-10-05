from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from langchain_core.documents import Document
from tqdm import tqdm


url = "https://www.ishtar-collective.net"


def crawl_categories():
    req = Request(f"{url}/categories", headers={"User-Agent": "Mozilla/5.0"})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, "html.parser")
    div = soup.findAll("div", {"class": "category-list"})
    categories = []
    for category in div:
        links = category.findAll("a")
        for link in links:
            categories.append(link.get("href"))
    # print(categories)
    return categories


def crawl_books():
    docs = []
    categories = crawl_categories()
    with tqdm(total=len(categories)) as categories_bar:
        for category in categories:
            categories_bar.set_description("category: " + category)

            req = Request(f"{url}{category}", headers={"User-Agent": "Mozilla/5.0"})
            html_page = urlopen(req).read()

            soup = BeautifulSoup(html_page, "html.parser")
            div = soup.findAll("div", {"class": "entry-thumbnail col-4"})

            links = []
            for ele in div:
                links.append(ele.find("a").get("href"))

            with tqdm(total=len(links), leave=False) as books_bar:
                for link in links:
                    books_bar.set_description("book: " + link)

                    req = Request(url + link, headers={"User-Agent": "Mozilla/5.0"})
                    html_page = urlopen(req).read()

                    soup = BeautifulSoup(html_page, "html.parser")
                    descriptions = soup.find(
                        "div", {"class": "description highlightable"}
                    )

                    paragraphs = descriptions.findAll("p")

                    category_regex = re.search(r"/categories/(.*)$", category).group(1)
                    regex = rf"\/entries\/([A-Za-z0-9\S]+)#{category_regex}"

                    metadata = {"source": re.search(regex, link).group(1)}
                    joined_content = " ".join(
                        [paragraph.text for paragraph in paragraphs]
                    )
                    docs.append(
                        Document(page_content=joined_content, metadata=metadata)
                    )
                    books_bar.update(1)

            categories_bar.update(1)

    return docs


if __name__ == "__main__":
    crawl_books()
