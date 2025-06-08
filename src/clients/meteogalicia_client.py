import json
import requests
from pathlib import Path

def fetch_meteogalicia_estaciones_reales(output_json):
    print("⏳ Descargando estaciones desde Rede_Estacions...")

    base_url = (
        "https://ideg.xunta.gal/meteogalicia/rest/services/"
        "Meteogalicia_Observacion/RedMeteorologica/MapServer/1/query"
    )

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
        response = requests.get(base_url, params=params)
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

    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✔ Estaciones guardadas en: {output_json}")
    print(f"📊 Total: {len(all_features)} estaciones")

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parents[2]
    output = ROOT / "data" / "raw" / "meteogalicia" / "estaciones_reales_meteogalicia.json"
    fetch_meteogalicia_estaciones_reales(output)
