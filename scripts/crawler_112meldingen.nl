#!/usr/bin/env python

import requests
import logging
import time
import json
import sys
import re
import os

from datetime import datetime

from bs4 import BeautifulSoup

BASE_URL = "http://www.112meldingen.nl"

ALRT_URL = BASE_URL + "/includes/alerts.php"
NEXT_URL = BASE_URL + "/index.php"

HEADERS = {"X-Requested-With": "XMLHttpRequest"}

TARGET_DIR = "dump_" + str(int(datetime.now().timestamp()))
if not os.path.exists(TARGET_DIR):
    os.mkdir(TARGET_DIR)

logging.basicConfig(
    filename=os.path.join(TARGET_DIR, "log.txt"),
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

logger = logging.getLogger("112meldingen_crawler")
if len(sys.argv) > 1:
    if sys.argv[1] == "log":
        logger.addHandler(logging.StreamHandler(sys.stdout))

session = requests.Session()
stopped = False


def remove_extra_spaces(text):
    return re.sub("[\xa0\s]+", " ", text)  # noqa: N605


# save every n batches
def save_batch(batch, data, target_dir, stopped):
    n = 10

    if batch % n == 0:
        name = "batches_{}-{}.json".format(batch - (n - 1), batch)
    elif stopped:
        name = "batches_{}-{}.json".format(batch - (batch % n), batch)
    else:
        return

    with open(os.path.join(target_dir, name), "w") as f:
        f.write(json.dumps(data))
    del data[:]


def parse_entries(entries):
    json_entry_list = []
    for entry in entries:
        data = {"units": []}

        trs = entry.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            entry_name = tds[1].text.strip()

            if entry_name == "melding":
                date_time = remove_extra_spaces(tds[0].text)

                data["time"] = date_time.split()[0]
                data["date"] = date_time.split()[1]

                n_parts = tds[3].find("a")
                if n_parts is not None:
                    data["link"] = BASE_URL + "/" + n_parts["href"]
                else:
                    n_parts = tds[3].find("span")

                data["notification"] = remove_extra_spaces(
                    ";".join(
                        [
                            c.text.strip() if hasattr(c, "text") else c.strip()
                            for c in n_parts
                        ]
                    )
                )
            if entry_name == "urgentie":
                u_parts = tds[3]
                data["urgency"] = remove_extra_spaces(
                    ";".join(
                        [
                            c.text.strip() if hasattr(c, "text") else c.strip()
                            for c in u_parts
                        ]
                    )
                )
            if entry_name == "regio":
                data["region"] = remove_extra_spaces(tds[3].text)
            if entry_name == "eenheden" or entry_name == "":
                data["units"].append(remove_extra_spaces(tds[3].text))

        json_entry_list.append(data)
    return json_entry_list


try:
    batch_nr = 1
    total = 0
    data = []

    while stopped is False:
        logger.info("Processing batch {}".format(batch_nr))
        r = session.get(ALRT_URL, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        entries = soup.find_all("table", {"id": "alerts"})

        data.extend(parse_entries(entries))
        total += len(entries)
        logger.info(
            "{} entries processed. Total entries: {})".format(len(entries), total)
        )

        save_batch(batch_nr, data, TARGET_DIR, stopped)
        batch_nr += 1

        for i in range(10):
            try:
                session.post(
                    NEXT_URL,
                    headers=HEADERS,
                    data={"submitFormNextAlerts": "vroeger+>>>"},
                )
                break
            except ConnectionError:
                logger.error(
                    "Advancing failed {} times. Waiting 1s and trying again...".format(i)
                )
                time.sleep(1)
            else:
                logger.error("Couldn't advance any further. Stopping...")
                stopped = True

except KeyboardInterrupt:
    stopped = True
finally:
    save_batch(batch_nr, data, TARGET_DIR, stopped)
