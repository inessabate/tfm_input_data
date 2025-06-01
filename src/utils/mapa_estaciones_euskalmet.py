
import json
import folium
from pathlib import Path

def generar_mapa_estaciones(json_path: str, output_html: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    mapa = folium.Map(location=[43.2, -2.5], zoom_start=8)

    for feature in data["features"]:
        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        nombre = props.get("nombre", "Sin nombre")
        municipio = props.get("municipio", "")
        popup_text = f"<b>{nombre}</b><br>{municipio}"

        folium.Marker(
            location=[coords[1], coords[0]],
            popup=popup_text,
            tooltip=nombre,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(mapa)

    # ✅ Asegurar que el directorio exista
    Path(output_html).parent.mkdir(parents=True, exist_ok=True)

    mapa.save(output_html)
    print(f"✔ Mapa guardado en: {output_html}")

if __name__ == "__main__":

    ROOT_DIR = Path(__file__).resolve().parents[2]  # tfm_apis_input_data/
    json_input = ROOT_DIR / "data" / "raw" / "euskalmet" / "estaciones_euskalmet_2025-06-01.json"
    html_output = ROOT_DIR / "data" / "maps" / "estaciones_euskalmet_mapa.html"
    generar_mapa_estaciones(json_input, html_output)
