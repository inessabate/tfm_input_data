import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from src.clients.siar_client import SiarClient
from src.clients.euskalmet_client import EuskalmetClient
from src.clients.meteogalicia_client import MeteoGaliciaClient
from src.clients.aemet_client import AemetClient

# Comment to commit something. Not useful at all.

def run_siar_for_aragon():
    siar_stations_aragon = [
        "HU01", "HU02", "HU03", "HU04", "HU05", "HU06", "HU07", "HU08", "HU09", "HU10"
    ]
    yesterday = datetime.today().date() - timedelta(days=1)
    day_before_yesterday = yesterday - timedelta(days=1)

    for day in [yesterday, day_before_yesterday]:
        try:
            siar = SiarClient(
                estaciones=siar_stations_aragon,
                fecha_inicial=str(day),
                fecha_final=str(day)
            )
            siar.ejecutar()
            break
        except Exception as e:
            print(f"❌ Unexpected error in SIAR ({day}): {e}")

def run_siar_stations():
    try:
        client = SiarClient()
        client.ejecutar()
    except Exception as e:
        print(f"❌ Error downloading SIAR stations: {e}")

def run_euskalmet():
    try:
        client = EuskalmetClient()
        client.ejecutar()
    except Exception as e:
        print(f"❌ Unexpected error in Euskalmet: {e}")

def run_meteogalicia():
    try:
        client = MeteoGaliciaClient()
        client.ejecutar()
    except Exception as e:
        print(f"❌ Unexpected error in MeteoGalicia: {e}")

def run_aemet():
    try:
        client = AemetClient()
        client.ejecutar()
    except Exception as e:
        print(f"❌ Unexpected error in AEMET: {e}")

if __name__ == "__main__":
    mode = "meteogalicia"  # ← Change this according to what you want to run


    if mode == "siar_aragon":
        run_siar_for_aragon()
    elif mode == "siar_stations":
        run_siar_stations()
    elif mode == "euskalmet":
        run_euskalmet()
    elif mode == "meteogalicia":
        run_meteogalicia()
    elif mode == "aemet":
        run_aemet()
    elif mode == "all":
        run_siar_for_aragon()
        run_siar_stations()
        run_euskalmet()
        run_meteogalicia()
        run_aemet()