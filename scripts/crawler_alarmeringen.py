#!/usr/bin/env python

import requests
import json
import re

from bs4 import BeautifulSoup


BASE_URL = "https://alarmeringen.nl"


def get_links():
    url = BASE_URL + "/noord-brabant/brabant-zuidoost/eindhoven/"
    links = []

    for page in range(1, 5):
        resp = requests.get(url + "?page={}".format(page))
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            found = 0
            for item in soup.find_all("a"):
                try:
                    content = (item["href"])
                    if "html" in content:
                        if len(content.split("/")) > 4:
                            links.append(content)
                            found += 1
                except KeyError:
                    pass
            print("Found {} on page {}".format(found, page))

    links = set(links)
    return links


def process_links(links):
    event_list = []

    for link in links:
        resp = requests.get(BASE_URL + link)
        try:
            if resp.status_code == 200:
                d = {}
                soup = BeautifulSoup(resp.content, "html.parser")
                container = soup.find("div", {"class": "ads-details-wrapper"})

                d["title"] = container.find("h1").text.strip()

                date = container.find("span", {"class": "date"}).text.strip()
                d["date"] = re.sub("\n.*", "", date)

                text = container.find_all("p")
                summary = text[0].b.text.strip()
                d["summary"] = re.sub("\n\s*", " ", summary)

                combined_p = ""
                for p in text[1:]:
                    combined_p += p.text.strip()

                d["content"] = re.sub("\n", " ", combined_p)

                event_list.append(d)
        except Exception:
            print("Error encountered processing {}".format(link))

    return event_list


links = get_links()
event_list = process_links(links)

with open("./data_dump.json", "w") as f:
    f.write(json.dumps(event_list))

print("Output written to ./data_dump.json")
