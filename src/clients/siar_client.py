import time

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
        self.url_observations = "https://servicio.mapama.gob.es/apisiar/API/v1/Datos/Diarios/Estacion"
        self.url_stations = "https://servicio.mapama.gob.es/apisiar/API/v1/Info/Estaciones"


    def fetch_datos_estacion(self, estacion_id):
        params = {
            "Id": estacion_id,
            "FechaInicial": self.fecha_inicial,
            "FechaFinal": self.fecha_final,
            "ClaveAPI": self.api_key
        }
        response = requests.get(self.url_observations, params=params)
        if response.status_code == 200:
            return response.json().get("Datos", [])
        else:
            raise RuntimeError(f"Error {response.status_code}: {response.text}")

    def get_daily_observations(self):
        # TODO: Implement a way to get all stations dinamically
        for est in self.estaciones:
            time.sleep(60)
            try:
                self.log(f"Retrieving data from station {est}")
                datos = self.fetch_datos_estacion(est)
                if datos:
                    self.save_json(
                        f"{self.name.upper()}_observations_{est}_{self.fecha_inicial}_{self.fecha_final}",
                        datos,
                        include_date=False
                    )
                else:
                    self.log(f"No data found for {est}")
            except Exception as e:
                self.log(f"❌ Error at {est}: {e}")

    def get_siar_stations(self):

        params = {"ClaveAPI": self.api_key}

        response = requests.get(self.url_stations, params=params)
        if response.status_code != 200:
            raise RuntimeError(f"Error when fetching stations {response.status_code} - {response.text}")

        stations_data: dict = response.json()
        stations_data: dict = stations_data["Datos"]

        # Save the stations data
        self.save_json(
            f"{self.name.upper()}_stations",
            stations_data,
            include_date=False
        )


    def ejecutar(self):
        self.log(f"Starting {self.name.upper()} download...")
        self.get_siar_stations()
        self.get_daily_observations()
        self.log(f"Finished data retrieval from {self.name.upper()}.")
