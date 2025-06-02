
import json
import folium
from pathlib import Path

def dms_to_decimal(dms_str: str, is_lat: bool) -> float:
    """Convierte una coordenada en formato DMS de AEMET (ej. '394924N') a decimal."""
    d = int(dms_str[:2])
    m = int(dms_str[2:4])
    s = int(dms_str[4:6])
    direction = dms_str[-1]

    decimal = d + m / 60 + s / 3600
    if (is_lat and direction == "S") or (not is_lat and direction == "W"):
        decimal *= -1
    return decimal

def generar_mapa_estaciones_combinado(path_euskalmet, path_aemet, output_html):
    # Mapa centrado en la península
    mapa = folium.Map(location=[40.0, -3.5], zoom_start=6)

    # ─── Euskalmet ─────────────────────────────────────────────────────────────
    with open(path_euskalmet, "r", encoding="utf-8") as f:
        euskalmet_data = json.load(f)

    for feature in euskalmet_data["features"]:
        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        nombre = props.get("nombre", "Sin nombre")
        municipio = props.get("municipio", "")
        popup_text = f"<b>{nombre}</b><br>{municipio}"

        folium.Marker(
            location=[coords[1], coords[0]],
            popup=popup_text,
            tooltip=nombre,
            icon=folium.Icon(color="blue", icon="cloud")
        ).add_to(mapa)

    # ─── AEMET ────────────────────────────────────────────────────────────────
    with open(path_aemet, "r", encoding="utf-8") as f:
        aemet_data = json.load(f)

    for est in aemet_data:
        try:
            lat = dms_to_decimal(est["latitud"], is_lat=True)
            lon = dms_to_decimal(est["longitud"], is_lat=False)
            nombre = est.get("nombre", "Sin nombre")
            provincia = est.get("provincia", "")
            popup_text = f"<b>{nombre}</b><br>{provincia}"

            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                tooltip=nombre,
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(mapa)
        except Exception as e:
            print(f"Error procesando estación AEMET: {est.get('nombre', 'sin nombre')} -> {e}")

    # Crear carpeta si no existe
    Path(output_html).parent.mkdir(parents=True, exist_ok=True)
    mapa.save(output_html)
    print(f"✔ Mapa combinado guardado en: {output_html}")

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    path_euskalmet = ROOT_DIR / "data" / "raw" / "euskalmet" / "estaciones_euskalmet_2025-06-01.json"
    path_aemet = ROOT_DIR / "data" / "raw" / "aemet" / "estaciones_aemet_2025-06-02.json"
    path_mapa = ROOT_DIR / "data" / "maps" / "mapa_estaciones_combinado.html"
    generar_mapa_estaciones_combinado(path_euskalmet, path_aemet, path_mapa)
