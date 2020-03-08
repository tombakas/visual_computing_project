#!/usr/bin/env python3

import json
import os
import re
import shutil

from glob import glob
from pprint import pprint
from datetime import datetime as dt


existing_codes = set()
strange_codes = set()

combined_batches = []
strange_batches = []


def read_batch_data(directory, glob_pattern):
    filenames = glob(os.path.join(directory, glob_pattern))

    for i, filename in enumerate(filenames):
        with open(filename) as f:
            batch_data = json.load(f)

        for batch in batch_data:
            postcode = batch["postcode"]
            if postcode not in existing_codes.union(strange_codes):

                if postcode == "0952TS":
                    pprint(batch)
                if re.match("[0-9]{4}[A-Z]{2}", postcode):
                    existing_codes.add(postcode)
                    combined_batches.append(batch)
                else:
                    strange_codes.add(postcode)
                    strange_batches.append(batch)
        print(f"Read file {i + 1} of {len(filenames)}", end="\r", flush=True)
    print("")


def write_done(now):
    if existing_codes:
        postcodes = list(existing_codes)
        postcodes.sort()

        target = os.path.join("postcode_categories", "done.txt")

        if os.path.exists(target):
            copy_name = os.path.join("postcode_categories", now + "done.txt")
            print(f"Making a copy of done.txt as {now + 'done.txt'}")
            shutil.copy(target, copy_name)

        with open(os.path.join("postcode_categories", "done.txt"), "w") as f:
            for postcode in postcodes:
                f.write(f"{postcode}\n")

        print(f"Written {len(postcodes)} entries to done.txt")


def save_batches(now):
    regular_name = now + "regular_postcodes.json"

    with open(regular_name, "w") as f:
        json.dump(combined_batches, f)

    print(f"Written {len(combined_batches)} entries to {regular_name}")

    strange_name = now + "strange_postcodes.json"
    with open(strange_name, "w") as f:
        json.dump(strange_batches, f)

    print(f"Written {len(strange_batches)} entries to {strange_name}")



# read text batches
print("Reading text batches:")
read_batch_data("batches", "*txt")

# read json batches
print("Reading json batches:")
read_batch_data("combined", "*json")

now = dt.now().strftime("%Y-%m-%d_%H:%M_")

write_done(now)
save_batches(now)
