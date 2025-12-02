import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "MyWikiScraper/1.0 (https://github.com/aseige03; andersonseigel1199@gmail.com)",
}

resp = requests.get('https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions',headers = headers).text

soup = BeautifulSoup(resp, 'html.parser')

tables = soup.find_all('table')

for table in tables:
  rows = table.find_all('tr')
  print(len(rows))