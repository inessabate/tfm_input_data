from src.clients.base_client import BaseClient
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

class SiarClient(BaseClient):
    def __init__(self, estaciones=None, fecha_inicial=None, fecha_final=None):
        load_dotenv()
        api_key = os.getenv("API_KEY_SIAR")
        if not api_key:
            raise ValueError("No se pudo cargar API_KEY_SIAR desde .env.")
        super().__init__("siar")
        self.api_key = api_key
        self.estaciones = estaciones or []
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.api_url = "https://servicio.mapama.gob.es/apisiar/API/v1/Datos/Diarios/Estacion"

    def fetch_datos_estacion(self, estacion_id):
        params = {
            "Id": estacion_id,
            "FechaInicial": self.fecha_inicial,
            "FechaFinal": self.fecha_final,
            "ClaveAPI": self.api_key
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json().get("Datos", [])
        else:
            raise RuntimeError(f"Error {response.status_code}: {response.text}")

    def descargar_mediciones(self):
        for est in self.estaciones:
            try:
                self.log(f"Retrieving data from station {est}")
                datos = self.fetch_datos_estacion(est)
                if datos:
                    self.save_json(f"measures_{est}", datos, include_date=False)
                else:
                    self.log(f"No data found for {est}")
            except Exception as e:
                self.log(f"❌ Error at {est}: {e}")

    def descargar_estaciones_siar(self):
        url = "https://servicio.mapama.gob.es/apisiar/api/v1/Estaciones"
        params = {"ClaveAPI": self.api_key}

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise RuntimeError(f"Error when fetching stations {response.status_code} - {response.text}")

        estaciones = response.json()
        registros = []

        for est in estaciones:
            registros.append({
                "id_estacion": est.get("IdEstacion"),
                "nombre": est.get("Nombre"),
                "latitud": est.get("Latitud"),
                "longitud": est.get("Longitud"),
                "provincia": est.get("Provincia"),
                "comunidad": est.get("ComunidadAutonoma")
            })

        df = pd.DataFrame(registros)
        output_path = Path("data/clean/estaciones_siar.xlsx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        print(f"✔ Listado de estaciones SIAR guardado en {output_path}")

    def ejecutar(self):
        self.log(f"Starting {self.name.upper()} download...")
        self.descargar_mediciones()
        self.log(f"Finished data retrieval from {self.name.upper()}.")
