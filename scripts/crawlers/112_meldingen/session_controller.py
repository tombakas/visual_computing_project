import requests

from bs4 import BeautifulSoup


BASE_URL = "http://www.112meldingen.nl"

ALRT_URL = BASE_URL + "/includes/alerts.php"
SETTINGS_URL = BASE_URL + "/index.php"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive"
}


class SessionController:

    def __init__(self):
        self.session = requests.Session()

    def get_html(self):
        ret = self.session.get(ALRT_URL, headers=HEADERS)
        return ret.text

    def modify_settings(self, settings):
        ret = self.session.post(
            SETTINGS_URL,
            headers=HEADERS,
            data=settings
        )
        if ret.status_code == 200:
            return True
        return False

    def get_entries(self):
        soup = BeautifulSoup(
            self.get_html(), "html.parser"
        )
        entries = soup.find_all("table", {"id": "alerts"})

        return entries

    def setup_regions(self, regions):
        settings = {"submitSettingRegions": "opslaan"}
        for region in regions:
            settings[region] = "on"
        return self.modify_settings(settings)

    def next(self):
        try:
            return self.modify_settings({"submitFormNextAlerts": "vroeger+>>>"})
        except requests.exceptions.ConnectionError:
            return False
