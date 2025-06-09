import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from src.clients.base_client import BaseClient

class AemetClient(BaseClient):
    def __init__(self):
        super().__init__("aemet")
        load_dotenv()
        self.api_key = os.getenv("API_KEY_AEMET")
        if not self.api_key:
            raise ValueError("API_KEY_AEMET not found in .env")
        self.headers = {
            "Accept": "application/json",
            "api_key": self.api_key
        }
        self.url_estaciones = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

    def obtener_estaciones(self):
        try:
            self.log("Requesting station inventory from AEMET...")
            resp = requests.get(self.url_estaciones, headers=self.headers)
            resp.raise_for_status()
            url_datos = resp.json().get("datos")
            if not url_datos:
                raise ValueError("Data URL not found in the initial response.")

            estaciones_resp = requests.get(url_datos)
            estaciones_resp.raise_for_status()
            estaciones_data = estaciones_resp.json()

            self.save_json("estaciones_aemet", estaciones_data)
            self.log(f"Total stations downloaded: {len(estaciones_data)}")

        except Exception as e:
            self.log(f"❌ Error getting stations: {e}")

    def ejecutar(self):
        self.log(f"Starting {self.name.upper()} download...")
        self.obtener_estaciones()
        self.log(f"Finished data retrieval from {self.name.upper()}.")