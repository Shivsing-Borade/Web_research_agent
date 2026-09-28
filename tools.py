from langchain_community.tools import DuckDuckGoSearchResults
import requests
from bs4 import BeautifulSoup

search = DuckDuckGoSearchResults(output_format="list")

def web_search(query: str):
    return search.invoke(query)


def scrape_page(url: str):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return text