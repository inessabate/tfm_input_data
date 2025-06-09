import json
import requests
from pathlib import Path
from src.clients.base_client import BaseClient

class MeteoGaliciaClient(BaseClient):
    def __init__(self):
        super().__init__("meteogalicia")
        self.base_url = (
            "https://ideg.xunta.gal/meteogalicia/rest/services/"
            "Meteogalicia_Observacion/RedMeteorologica/MapServer/1/query"
        )

    def get_stations(self):
        print("⏳ Descargando estaciones desde Rede_Estacions...")

        params = {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
            "f": "json",
            "resultOffset": 0,
            "resultRecordCount": 2000
        }

        all_features = []
        while True:
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                self.log(f"❌ Error in retrieving stations: {response.status_code} - {response.text}")
                break

            data = response.json()
            features = data.get("features", [])
            if not features:
                self.log(f"Download finished")
                break

            all_features.extend(features)
            self.log(f"🔄Total stations retrieved: {len(features)} ")
            params["resultOffset"] += params["resultRecordCount"]

        result = {
            "type": "FeatureCollection",
            "features": all_features
        }

        self.save_json("stations_meteogalicia", result, include_date=False)


    def ejecutar(self):
        self.log(f"Starting {self.name.upper()} download...")
        self.get_stations()
        self.log(f"Finished data retrieval from {self.name.upper()}.")
