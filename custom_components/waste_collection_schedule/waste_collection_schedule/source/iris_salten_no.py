import datetime
import requests
import json
from waste_collection_schedule import Collection

TITLE = "Iris Salten" # Title will show up in README.md and info.md
DESCRIPTION = "Source script for iris-salten.no"  # Describe your source
URL = "https://www.iris-salten.no/"  # Insert url to service homepage. URL will show up in README.md and info.md
TEST_CASES = {
    "Test 1": { "estateid": "5263446d-e66c-4c5b-ba9a-14054403d9f9" }
}

API_URL = "https://iristk.iris-salten.no:8084/api/"
APP_ID = "95b6459a-5756-4dc8-8b05-423da7850fd5"
HOST_ID = "100"

ICON_MAP = {
    "9999": "mdi:trash-can",                  # Restavfall
    "2110": "mdi:leaf",                       # Matavfall
    "2400": "mdi:newspaper-variant-multiple", # Papir og papp
    "2612": "mdi:recycle",                    # Glass- og metallemballasje
    "3200": "mdi:recycle",                    # Plast
    "101":  "mdi:sack",                       # Julesekken
    "100":  "mdi:pine-tree"                   # Juletre
}

class Source:
    def __init__(self, estateid):
        self._estateid = estateid
        self._token = None

    def _login(self):
        data = {
             "applikasjonsId": APP_ID,
             "oppdragsgiverId": HOST_ID
        }

        r = requests.post(API_URL + "login", json=data)
        self._token = r.headers['Token']

    def fetch(self):
        if self._token is None:
            self._login();

        headers = {
            'Token': self._token
        }

        today = datetime.date.today()
        nextyear = today + datetime.timedelta(days=365.25)

        args = {
            'eiendomId': self._estateid,
            'datoFra': today.strftime("%Y-%m-%d"),
            'datoTil': nextyear.strftime("%Y-%m-%d")
        }

        r = requests.get(API_URL + 'tomminger', params = args, headers = headers)
        entries = []
        for f in json.loads(r.content):
            entries.append(
                Collection(
                    date = datetime.datetime.strptime(f['dato'], "%Y-%m-%dT%H:%M:%S").date(),
                    t = f['fraksjon'],
                    icon = ICON_MAP.get(f['fraksjonId'])
                )
            )

        return entries
