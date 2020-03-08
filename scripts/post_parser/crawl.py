#!/usr/bin/env python3

import os
import json
import requests
import logging

from time import time, sleep

# TOKEN = "4bbb76996d4ef9"
# TOKEN = "93c848df7e94ce"
TOKEN = "069085661d02d2"
BATCH_SIZE = 10
INTERVAL_SLEEP = 0.6
CATEGORY_DIR = "postcode_categories"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="crawl.log",
                    filemode="w")

url = "https://eu1.locationiq.com/v1/search.php"
params = {
    "key": TOKEN,
    "format": "json",
    # "country": "netherlands"
}


def get_text_file(name):
    return os.path.join(CATEGORY_DIR, name)

def write_unknown_to_file():
    with open(get_text_file("unknown.txt"), "w") as f:
        for entry in unknown_codes:
            f.write("{}\n".format(entry.strip()))

with open(get_text_file("todo.txt")) as f:
    todo = f.read().split()

with open(get_text_file("done.txt")) as f:
    done = f.read().split()

with open(get_text_file("unknown.txt")) as f:
    unknown_codes = set()
    for item in f:
        unknown_codes.add(item.strip())


def append_done(batch):
    global done
    with open(get_text_file("done.txt"), "a") as f:
        for item in batch:
            done.append(item["postcode"])
            f.write(item["postcode"] + "\n")


batch_count = 1
def save_batch(batch):
    global batch_count

    if not os.path.exists("batches"):
        os.makedirs("batches")

    filename = os.path.join("batches", str(int(time())) + ".txt")
    with open(filename, "w") as f:
        json.dump(batch, f)

    logging.info("Written batch " + str(batch_count))
    batch_count += 1
    append_done(batch)
    batch = {}


stop = False
too_fast = 2
current_batch = []

def get_codes():
    global stop
    global too_fast
    global current_batch

    skip_count = 0
    for item in todo:
        if item not in done and item not in unknown_codes:
            if skip_count:
                logging.info("Skipped " + str(skip_count) + " entries.")
                skip_count = 0
            params["q"] = item
            response = requests.get(url, params=params)
            response.raise_for_status()
            too_fast = 2

            response_json = response.json()[0]
            response_json["postcode"] = item
            current_batch.append(response_json)

            sleep(INTERVAL_SLEEP)
            if len(current_batch) >= BATCH_SIZE:
                save_batch(current_batch)
                current_batch = []
        else:
            skip_count += 1
        if stop:
            break
    stop = True

while not stop:
    try:
        get_codes()

    except KeyboardInterrupt:
        stop = True
        logging.info("Keyboard interrupt received. Stopping...")
        print("Keyboard interrupt received. Stopping...")
    except requests.exceptions.HTTPError as e:
        if len(current_batch):
            save_batch(current_batch)

        # Too many requests
        if e.response.status_code == 429:
            logging.info("Went too fast! ")
            too_fast += 1

            logging.info("Sleeping for " + str(too_fast * 5) + " seconds.")
            sleep(too_fast * 5)
            logging.info("Restarting.")

        # Postcode/address does not exist
        if e.response.status_code == 404:
            code = e.response.url[-6:]
            unknown_codes.add(code)
            logging.info("Unknown postcode: " + code)
        else:
            print(e)

print("Saving out unknown codes...")
write_unknown_to_file()
print("Done.")
