import requests
from bs4 import BeautifulSoup
import csv
import re

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {
    "User-Agent": "MyWikiScraper/1.0 (https://github.com/aseige03; andersonseigel1199@gmail.com)"
}

def clean_text(el):
    if el is None:
        return ""
    text = el.get_text(separator=" ", strip=True)
    # remove bracketed footnotes like [1], [a]
    text = re.sub(r"\[.*?\]", "", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    tables = soup.find_all("table")
    # choose largest table by number of tr rows
    table = max(tables, key=lambda t: len(t.find_all("tr")))

    rows = table.find_all("tr")

    # find header row (first tr that has th elements)
    header_cells = None
    header_index = 0
    for i, r in enumerate(rows):
        ths = r.find_all("th")
        if ths:
            header_cells = ths
            header_index = i
            break

    if header_cells is None:
        # fallback: use first row's cells as header
        header_cells = rows[0].find_all(["td", "th"])
        header_index = 0

    headers = [clean_text(c) for c in header_cells]

    data_rows = []
    for r in rows[header_index + 1 :]:
        cells = r.find_all(["td", "th"])
        if not cells:
            continue
        row = [clean_text(c) for c in cells]
        data_rows.append(row)

    # determine max columns to normalize rows
    max_cols = max(len(headers), *(len(r) for r in data_rows))
    if len(headers) < max_cols:
        # expand headers with placeholders
        headers += [f"col_{i}" for i in range(len(headers), max_cols)]

    # pad rows
    norm_rows = [r + [""] * (max_cols - len(r)) for r in data_rows]

    out_path = "superbowl_champions.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(norm_rows)

    print(f"Wrote {len(norm_rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
