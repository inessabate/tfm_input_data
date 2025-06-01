
from datetime import datetime, timedelta
from src.clients.siar_client import SiarClient
from src.clients.euskalmet_client import EuskalmetClient
from src.clients.meteogalicia_client import MeteoGaliciaClient

def run_siar_for_aragon():
    estaciones_siar_aragon = [
        "HU01", "HU02", "HU03", "HU04", "HU05", "HU06", "HU07", "HU08", "HU09", "HU10",
        #"HU11", "HU12", "HU13", "HU14", "HU15", "HU17", "HU18", "HU19", "HU20", "HU21", "HU22"
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
            break  # solo ejecuta con ayer o anteayer
        except Exception as e:
            print(f"❌ Error inesperado en SIAR ({dia}): {e}")

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

if __name__ == "__main__":
    #run_siar_for_aragon()
    run_euskalmet()
    #run_meteogalicia()
