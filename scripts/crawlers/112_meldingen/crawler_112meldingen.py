#!/usr/bin/env python

import logging
import time
import sys
import os

from functions import (
    parse_entries,
    save_batch,
    get_logger,
)

from constants import (
    TARGET_DIR,
    REGIONS,
    SERVICE_SETTINGS
)

from session_controller import SessionController

def setup(verbose=False):
    if not os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)
    logger = get_logger()
    if verbose:
        logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger


def run(verbose=False, date_settings=None):
    stop = False
    error = False
    sc = SessionController()
    sc.get_entries()
    logger = setup(verbose)

    if not all([
        sc.setup_regions(REGIONS),
        sc.modify_settings(SERVICE_SETTINGS)
    ]):
        logger.error("Can't configure settings")
        stop = True
        error = True

    if date_settings:
        if not sc.modify_settings(date_settings):
            logger.error("Can't configure settings")
            stop = True
            error = True

    try:
        batch_nr = 1
        total = 0
        data = []

        while stop is False:

            logger.info("Processing batch {}".format(batch_nr))

            entries = sc.get_entries()

            if len(entries) == 0:
                logger.error("No data")
                stop = True
                error = True

            data.extend(parse_entries(entries, logger))
            total += len(entries)

            logger.info(
                "{} entries processed. Total entries: {})".format(len(entries), total)
            )

            if not error:
                save_batch(batch_nr, data, TARGET_DIR, stop)
            batch_nr += 1

            for i in range(10):
                if sc.next():
                    break

                logger.error(
                    "Advancing failed {} times. Waiting 1s and trying again...".format(i)
                )
                time.sleep(1)

                if i == 9:
                    stop = True

    except KeyboardInterrupt:
        stop = True
    finally:
        if not error:
            save_batch(batch_nr, data, TARGET_DIR, stop)
