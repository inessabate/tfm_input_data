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

        output_path = Path("data/raw/meteogalicia/estaciones_reales_meteogalicia.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"✔ Estaciones guardadas en: {output_path}")
        print(f"📊 Total: {len(all_features)} estaciones")

    def ejecutar(self):
        self.fetch_estaciones_reales()
