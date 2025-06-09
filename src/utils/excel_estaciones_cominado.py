import json
import pandas as pd
from pathlib import Path
from pyproj import Transformer
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def dms_to_decimal(dms_str: str, is_lat: bool) -> float:
    d = int(dms_str[:2])
    m = int(dms_str[2:4])
    s = int(dms_str[4:6])
    direction = dms_str[-1]
    decimal = d + m / 60 + s / 3600
    if (is_lat and direction == "S") or (not is_lat and direction == "W"):
        decimal *= -1
    return decimal


def extraer_estaciones(path_euskalmet, path_aemet, path_meteogalicia, output_excel):
    registros = []

    # Euskalmet
    with open(path_euskalmet, "r", encoding="utf-8") as f:
        data = json.load(f)
    for feature in data["features"]:
        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        registros.append({
            "id_estacion": props.get("id") or props.get("codigo", ""),
            "estacion": props.get("nombre", "Sin nombre"),
            "latitud": coords[1],
            "longitud": coords[0],
            "fuente": "Euskalmet"
        })

    # AEMET
    with open(path_aemet, "r", encoding="utf-8") as f:
        data = json.load(f)
    for est in data:
        try:
            lat = dms_to_decimal(est["latitud"], is_lat=True)
            lon = dms_to_decimal(est["longitud"], is_lat=False)
            registros.append({
                "id_estacion": est.get("indicativo", ""),
                "estacion": est.get("nombre", "Sin nombre"),
                "latitud": lat,
                "longitud": lon,
                "fuente": "AEMET"
            })
        except Exception as e:
            print(f"❌ Error AEMET: {est.get('nombre')} -> {e}")

    # MeteoGalicia
    with open(path_meteogalicia, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformer = Transformer.from_crs("EPSG:25829", "EPSG:4326", always_xy=True)
    for feature in data["features"]:
        attr = feature["attributes"]
        geom = feature["geometry"]
        try:
            lon, lat = transformer.transform(geom["x"], geom["y"])
            registros.append({
                "id_estacion": attr.get("idEstacion", ""),
                "estacion": attr.get("Estacion", "Sin nombre"),
                "latitud": lat,
                "longitud": lon,
                "fuente": "MeteoGalicia"
            })
        except Exception as e:
            print(f"❌ Error en MeteoGalicia ({attr.get('Estacion')}): {e}")

    df = pd.DataFrame(registros)
    df.drop_duplicates(subset=["id_estacion", "latitud", "longitud", "fuente"], inplace=True)

    # --- Añadir códigos postales usando geopy ---
    print("⏳ Consultando códigos postales (esto puede tardar ~20 minutos)...")
    geolocator = Nominatim(user_agent="tfm-geocoder")
    geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1, max_retries=2, error_wait_seconds=5)

    codigos_postales = []
    for i, row in df.iterrows():
        lat, lon = row["latitud"], row["longitud"]
        try:
            location = geocode((lat, lon), language="es", exactly_one=True, addressdetails=True)
            cp = location.raw['address'].get("postcode") if location else None
        except Exception as e:
            print(f"⚠️ Error geocodificando ({lat}, {lon}): {e}")
            cp = None
        codigos_postales.append(cp)
        print(f"[{i + 1}/{len(df)}] {row['estacion']} → CP: {cp}")

    df["codigo_postal"] = codigos_postales

    # Guardar Excel
    Path(output_excel).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_excel, index=False)
    print(f"\n✔ Excel final guardado en: {output_excel}")
    print(f"📊 Total estaciones: {len(df)}")


if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    path_euskalmet = ROOT_DIR / "data" / "raw" / "euskalmet" / "estaciones_euskalmet_2025-06-08.json"
    path_aemet = ROOT_DIR / "data" / "raw" / "aemet" / "estaciones_aemet_2025-06-08.json"
    path_meteogalicia = ROOT_DIR / "data" / "raw" / "meteogalicia" / "estaciones_reales_meteogalicia.json"
    output_excel = ROOT_DIR / "data" / "clean" / "estaciones_combinadas_cp.xlsx"

    extraer_estaciones(path_euskalmet, path_aemet, path_meteogalicia, output_excel)
