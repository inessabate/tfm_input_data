import json
import pandas as pd
from pathlib import Path
from pyproj import Transformer

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

    # MeteoGalicia (fuente real con coordenadas UTM)
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

    # Crear DataFrame y exportar
    df = pd.DataFrame(registros)

    # Eliminar duplicados por seguridad
    df.drop_duplicates(subset=["id_estacion", "latitud", "longitud", "fuente"], inplace=True)

    Path(output_excel).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_excel, index=False)
    print(f"✔ Excel guardado en: {output_excel}")
    print(f"📊 Total estaciones: {len(df)}")

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    path_euskalmet = ROOT_DIR / "data" / "raw" / "euskalmet" / "estaciones_euskalmet_2025-06-08.json"
    path_aemet = ROOT_DIR / "data" / "raw" / "aemet" / "estaciones_aemet_2025-06-08.json"
    path_meteogalicia = ROOT_DIR / "data" / "raw" / "meteogalicia" / "estaciones_reales_meteogalicia.json"
    output_excel = ROOT_DIR / "data" / "clean" / "estaciones_combinadas.xlsx"

    extraer_estaciones(path_euskalmet, path_aemet, path_meteogalicia, output_excel)
