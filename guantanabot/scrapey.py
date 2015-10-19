from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pdb
import time
import json
import datetime
import random


def try_request(url):
    num_attempts = 5
    for i in range(num_attempts):
        try:
            html = urlopen(url)
        except:
            time.sleep(5)

    return html


def extract_details(prisoner_html):
    pris_details = BeautifulSoup(prisoner_html, "lxml")
    divs = pris_details.find_all("div", {"class": "nytint-detainee-fullcol"})

    for test in divs:
        try:
            name = test.find("h1").get_text().strip()
            country = test.find("a", href=re.compile("/country/")).get_text()
            time_in_gitmo = test.find(text=re.compile("for \d+ years")).lstrip(
                "for ").strip().rsplit(".\n\n", 1)[0]
        except:
            return None

    return {"name": name,
            "country": country,
            "time_in_gitmo": time_in_gitmo}


def main():
    base_url = "http://projects.nytimes.com"
    index_ref = "/guantanamo/detainees/current"
    index_html = urlopen(base_url + index_ref)
    index = BeautifulSoup(index_html, "lxml")

    prisoner_links = index.find_all(
        "a", href=re.compile("/guantanamo/detainees/\d+"))

    time_scraped = datetime.datetime.now()

    data = {}
    for each in prisoner_links:
        print('.')
        prisoner_html = try_request(base_url + each["href"])
        details = extract_details(prisoner_html)
        if details is not None:
            data[details["name"]] = {
                "country": details["country"],
                "time_in_gitmo": details["time_in_gitmo"],
                "tweet": ("{} from {} has been in Guantanamo Bay "
                          "for {}").format(details["name"],
                                           details["country"],
                                           details["time_in_gitmo"])}
        time.sleep(random.randint(0, 9))

    data["time_scraped"] = datetime.datetime.now().isoformat()

    with open("prisoners.json", "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    main()
