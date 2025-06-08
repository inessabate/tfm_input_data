import pandas as pd
import folium
from folium.plugins import MarkerCluster
from pathlib import Path

def generar_mapa_desde_excel(path_excel, path_output_html):
    df = pd.read_excel(path_excel)
    mapa = folium.Map(location=[40.0, -3.5], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(mapa)

    colores = {
        "AEMET": "green",
        "Euskalmet": "blue",
        "MeteoGalicia": "red"
    }

    for _, row in df.iterrows():
        try:
            nombre = row["estacion"]
            lat = row["latitud"]
            lon = row["longitud"]
            fuente = row["fuente"]
            popup = f"<b>{nombre}</b><br>{fuente}"
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=nombre,
                icon=folium.Icon(color=colores.get(fuente, "gray"))
            ).add_to(marker_cluster)
        except Exception as e:
            print(f"❌ Error con estación {row.get('estacion', 'sin nombre')}: {e}")

    # Añadir leyenda
    leyenda = """
    <div style="
        position: fixed; bottom: 50px; left: 50px; width: 180px; height: 120px;
        background-color: white; z-index:9999; font-size:14px;
        border:2px solid grey; padding: 10px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <b>🗺️ Leyenda</b><br>
        <i class="fa fa-map-marker fa-2x" style="color:green"></i> AEMET<br>
        <i class="fa fa-map-marker fa-2x" style="color:blue"></i> Euskalmet<br>
        <i class="fa fa-map-marker fa-2x" style="color:red"></i> MeteoGalicia
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda))

    Path(path_output_html).parent.mkdir(parents=True, exist_ok=True)
    mapa.save(path_output_html)
    print(f"✔ Mapa guardado en: {path_output_html}")

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parents[2]
    path_excel = ROOT / "data" / "clean" / "estaciones_combinadas.xlsx"
    path_html = ROOT / "data" / "maps" / "mapa_estaciones_combinadas.html"
    generar_mapa_desde_excel(path_excel, path_html)
