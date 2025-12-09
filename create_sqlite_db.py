import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import os

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {
    "User-Agent": "MyWikiScraper/1.0 (https://github.com/aseige03; andersonseigel1199@gmail.com)"
}

def clean_text(el):
    if el is None:
        return ""
    text = el.get_text(separator=" ", strip=True)
    text = re.sub(r"\[.*?\]", "", text)  # remove footnotes
    text = re.sub(r"\s+", " ", text).strip()
    return text

def make_colname(header: str, used: set, idx: int) -> str:
    # sanitize header to a safe sqlite column name
    name = header.strip()
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = name.lower().strip('_')
    if not name:
        name = f"col_{idx}"
    if re.match(r"^[0-9]", name):
        name = "c_" + name
    orig = name
    i = 1
    while name in used:
        name = f"{orig}_{i}"
        i += 1
    used.add(name)
    return name


def main():
    print("Fetching page...")
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    tables = soup.find_all("table")
    # pick largest table by number of <tr>
    table = max(tables, key=lambda t: len(t.find_all("tr")))
    rows = table.find_all("tr")

    # find header row
    header_cells = None
    header_index = 0
    for i, r in enumerate(rows):
        ths = r.find_all("th")
        if ths:
            header_cells = ths
            header_index = i
            break
    if header_cells is None:
        header_cells = rows[0].find_all(["td","th"])
        header_index = 0

    headers = [clean_text(c) for c in header_cells]
    # build normalized column names
    used = set()
    colnames = [make_colname(h, used, i) for i, h in enumerate(headers)]

    data_rows = []
    for r in rows[header_index+1:]:
        cells = r.find_all(["td","th"])
        if not cells:
            continue
        data_rows.append([clean_text(c) for c in cells])

    # normalize rows to max columns
    max_cols = max(len(colnames), *(len(r) for r in data_rows)) if data_rows else len(colnames)
    if len(colnames) < max_cols:
        for i in range(len(colnames), max_cols):
            colnames.append(make_colname(f"col_{i}", used, i))

    norm_rows = [r + [""] * (max_cols - len(r)) for r in data_rows]

    db_path = "superbowl.db"
    # remove existing DB to replace
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # create table
    cols_def = ", ".join(f'"{c}" TEXT' for c in colnames)
    create_sql = f"CREATE TABLE superbowl_champions ({cols_def});"
    cur.execute(create_sql)

    # insert rows
    placeholders = ",".join(["?"] * len(colnames))
    insert_sql = f"INSERT INTO superbowl_champions VALUES ({placeholders});"
    cur.executemany(insert_sql, norm_rows)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM superbowl_champions;")
    count = cur.fetchone()[0]
    conn.close()

    print(f"Wrote {count} rows to database '{db_path}' (table: superbowl_champions)")


if __name__ == "__main__":
    main()
