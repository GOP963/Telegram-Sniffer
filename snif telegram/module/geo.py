import requests
from bs4 import BeautifulSoup

def module_location(ip):
    url = f"https://www.iplocation.net/ip-lookup?query={ip}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    tables = soup.find_all("table")

    for tbl in tables:
        rows = tbl.find_all("tr")
        data = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                data[cols[0].text.strip()] = cols[1].text.strip()
        if data:
            print(data)
