import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {
    "User-Agent": "MyWikiScraper/1.0 (https://github.com/aseige03; andersonseigel1199@gmail.com)"
}

# Fetch the page
resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# Find all tables and pick the one with the most <tr> rows
tables = soup.find_all("table")
max_idx = 0
max_count = -1
for i, t in enumerate(tables):
    cnt = len(t.find_all("tr"))
    if cnt > max_count:
        max_count = cnt
        max_idx = i

table = tables[max_idx]
print(f"Selected table index {max_idx} with {max_count} rows")
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {
    "User-Agent": "MyWikiScraper/1.0 (https://github.com/aseige03; andersonseigel1199@gmail.com)"
}

def fetch_page(url: str, timeout: int = 10) -> BeautifulSoup | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()                     # raise on 4xx/5xx
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

    # parse HTML with BeautifulSoup and return soup
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup

def main():
    soup = fetch_page(URL)
    if soup is None:
        print("Failed to fetch page.")
        return

    # quick sanity checks
    print("Title:", soup.title.string.strip() if soup.title else "No title found")
    print("Page length (chars):", len(resp_text := soup.prettify()))

    # example: count tables on the page
    tables = soup.find_all("table")
    print("Found", len(tables), "tables")

if __name__ == "__main__":
    main()