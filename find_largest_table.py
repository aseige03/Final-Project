import requests
from bs4 import BeautifulSoup
from typing import Optional, Tuple

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {
    "User-Agent": "MyWikiScraper/1.0 (https://github.com/aseige03; andersonseigel1199@gmail.com)"
}


def fetch_page(url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

    return BeautifulSoup(resp.text, "html.parser")


def find_largest_table(soup: BeautifulSoup) -> Optional[Tuple[int, BeautifulSoup, int]]:
    tables = soup.find_all("table")
    if not tables:
        return None

    max_idx = None
    max_count = -1
    for i, table in enumerate(tables):
        rows = table.find_all("tr")
        count = len(rows)
        if count > max_count:
            max_count = count
            max_idx = i

    return (max_idx, tables[max_idx], max_count) if max_idx is not None else None


def main() -> None:
    soup = fetch_page(URL)
    if soup is None:
        print("Failed to fetch page.")
        return

    title = soup.title.string.strip() if soup.title and soup.title.string else "(no title)"
    print(f"Page title: {title}")

    result = find_largest_table(soup)
    if result is None:
        print("No tables found on the page.")
        return

    idx, table, rows_count = result
    print(f"Largest table index: {idx} with {rows_count} <tr> rows")

    rows = table.find_all("tr")
    print("First 10 rows cell counts (counting th+td):")
    for r_index, row in enumerate(rows[:10]):
        cells = row.find_all(["td", "th"])
        sample_text = ' | '.join([c.get_text(strip=True) for c in cells[:3]])
        print(f" row {r_index}: {len(cells)} cells; sample: {sample_text}")


if __name__ == "__main__":
    main()
