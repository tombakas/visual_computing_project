import re
import os
import json
import logging

from session_controller import BASE_URL
from constants import TARGET_DIR


def remove_extra_spaces(text):
    return re.sub("[\xa0\s]+", " ", text)  # noqa: N605


def establish_service(short_name):
    services = {
        "CM": "police",
        "CP": "ambulance",
        "CE": "fire-brigade",
        "CH": "helicopter"
    }

    if short_name in services:
        return services[short_name]
    else:
        return "unknown"


def parse_entries(entries, logger:logging.Logger):
    json_entry_list = []
    for entry in entries:
        data = {"units": []}

        trs = entry.find_all("tr")
        for tr in trs:
            try:
                tds = tr.find_all("td")
                entry_name = tds[1].text.strip()

                if entry_name == "melding":
                    date_time = remove_extra_spaces(tds[0].text)

                    data["time"] = date_time.split()[0]
                    data["date"] = date_time.split()[1]

                    n_parts = tds[3].find("a")
                    if n_parts is not None:
                        data["link"] = BASE_URL + "/" + n_parts["href"]
                        data["service"] = establish_service(n_parts["class"][0])
                    else:
                        n_parts = tds[3].find("span")
                        data["service"] = "unknown"

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
            except IndexError:
                logger.error("Error processing entry")
                logger.error("trs: {}".format(trs))
                logger.error("data: {}".format(data))

        json_entry_list.append(data)
    return json_entry_list


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


def get_logger():
    logging.basicConfig(
        filename=os.path.join(TARGET_DIR, "log.txt"),
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO
    )

    logger = logging.getLogger("112meldingen_crawler")

    return logger
