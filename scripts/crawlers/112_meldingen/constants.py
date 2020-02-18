from datetime import datetime


TARGET_DIR = "dump_" + str(int(datetime.now().timestamp()))
REGIONS = ["R09", "R22"]

SERVICE_SETTINGS = {
    "BRW":  "on",
    "cBrw": "E",
    "CPA": "on",
    "cCpa": "P",
    "POL": "on",
    "cPol": "M",
    "cKnr": "J",
    "TRA": "on",
    "cTra": "H",
    "cKwc": "G",
    "cLma": "D",
    "submitSettingServices": "opslaan",
}
