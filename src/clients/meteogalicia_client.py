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

    def fetch_estaciones_reales(self):
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
                print(f"❌ Error {response.status_code}: {response.text[:300]}")
                break

            data = response.json()
            features = data.get("features", [])
            if not features:
                print("✅ Descarga finalizada.")
                break

            all_features.extend(features)
            print(f"🔄 Total acumulado: {len(all_features)}")
            params["resultOffset"] += params["resultRecordCount"]

        result = {
            "type": "FeatureCollection",
            "features": all_features
        }

        self.save_json("estaciones_meteogalicia", result, include_date=False)


    def ejecutar(self):
        self.log(f"Starting {self.name.upper()} download...")
        self.fetch_estaciones_reales()
        self.log(f"Finished data retrieval from {self.name.upper()}.")
