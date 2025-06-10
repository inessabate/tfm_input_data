
from src.clients.base_client import BaseClient

import requests
import re
import json

class EuskalmetClient(BaseClient):
    def __init__(self):
        super().__init__("euskalmet")

        self.url_stations= "https://opendata.euskadi.eus/contenidos/ds_meteorologicos/estaciones_meteorologicas/opendata/estaciones-padding.geojson"
        #self.url_daily_observations = "https://opendata.euskadi.eus/contenidos_recurso/opendata/meteorologia_lecturas/opendata/.json"

    def get_stations(self):
        try:
            response = requests.get(self.url_stations)
            response.raise_for_status()
            raw_text = response.text

            match = re.search(r'jsonCallback\(\s*(\{.*\})\s*\)', raw_text, flags=re.DOTALL)
            if match:
                json_text = match.group(1)
                data = json.loads(json_text)
                self.save_json(f"{self.name.upper()}_stations", data, include_date=False)
            else:

                self.log("❌ Could not extract JSON from jsonCallback(...)")
        except Exception as e:
            self.log(f" ❌ Error in retrieving stations: {e}")

    def get_daily_observations(self):
        """
        Download daily observations from Euskalmet and save them as JSON.
        The URL for measurements is not provided in the original code, so this method
        is a placeholder. You may need to adjust the URL based on actual API documentation.
        """
        try:
            response = requests.get(self.url_daily_observations)
            response.raise_for_status()
            self.save_json(
                f"{self.name.upper()}_observations",
                response.json(),
                include_date=True
            )
        except Exception as e:
            self.log(f"❌ Error in retrieving daily observations: {e}")

    def ejecutar(self):
        """
        Execute the Euskalmet client to download stations and measurements.
        """
        self.log(f"\nStarting {self.name.upper()} download...")
        self.get_stations()
        self.get_daily_observations()
        self.log(f"Finished data retrieval from {self.name.upper()}.")
