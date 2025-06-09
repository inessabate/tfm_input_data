from datetime import datetime, timedelta
from src.clients.siar_client import SiarClient
from src.clients.euskalmet_client import EuskalmetClient
from src.clients.meteogalicia_client import MeteoGaliciaClient
from src.clients.aemet_client import AemetClient

def run_siar_for_aragon():
    estaciones_siar_aragon = [
        "HU01", "HU02", "HU03", "HU04", "HU05", "HU06", "HU07", "HU08", "HU09", "HU10"
    ]
    ayer = datetime.today().date() - timedelta(days=1)
    anteayer = ayer - timedelta(days=1)

    for dia in [ayer, anteayer]:
        try:
            siar = SiarClient(
                estaciones=estaciones_siar_aragon,
                fecha_inicial=str(dia),
                fecha_final=str(dia)
            )
            siar.ejecutar()
            break
        except Exception as e:
            print(f"❌ Error inesperado en SIAR ({dia}): {e}")

def run_siar_estaciones():
    try:
        client = SiarClient()
        client.descargar_estaciones_siar()
    except Exception as e:
        print(f"❌ Error descargando estaciones SIAR: {e}")

def run_euskalmet():
    try:
        client = EuskalmetClient()
        client.ejecutar()
    except Exception as e:
        print(f"❌ Error inesperado en Euskalmet: {e}")

def run_meteogalicia():
    try:
        client = MeteoGaliciaClient()
        client.ejecutar()
    except Exception as e:
        print(f"❌ Error inesperado en MeteoGalicia: {e}")

def run_aemet():
    try:
        client = AemetClient()
        client.ejecutar()
    except Exception as e:
        print(f"❌ Error inesperado en AEMET: {e}")

if __name__ == "__main__":
    modo = "siar_estaciones"  # ← Cambia esto según lo que quieras ejecutar

    if modo == "siar_aragon":
        run_siar_for_aragon()
    elif modo == "siar_estaciones":
        run_siar_estaciones()
    elif modo == "euskalmet":
        run_euskalmet()
    elif modo == "meteogalicia":
        run_meteogalicia()
    elif modo == "aemet":
        run_aemet()
    elif modo == "todo":
        run_siar_for_aragon()
        run_siar_estaciones()
        run_euskalmet()
        run_meteogalicia()
        run_aemet()
