
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
            raise ValueError("API_KEY_AEMET no encontrada en .env")
        self.headers = {
            "Accept": "application/json",
            "api_key": self.api_key
        }
        self.url_estaciones = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

    def obtener_estaciones(self):
        try:
            self.log("Solicitando inventario de estaciones a AEMET...")
            resp = requests.get(self.url_estaciones, headers=self.headers)
            resp.raise_for_status()
            url_datos = resp.json().get("datos")
            if not url_datos:
                raise ValueError("No se encontró la URL de datos en la respuesta inicial.")

            estaciones_resp = requests.get(url_datos)
            estaciones_resp.raise_for_status()
            estaciones_data = estaciones_resp.json()

            self.guardar_json("estaciones_aemet", estaciones_data)
            self.log(f"Total estaciones descargadas: {len(estaciones_data)}")

        except Exception as e:
            self.log(f"❌ Error al obtener estaciones: {e}")

    def ejecutar(self):
        self.log("Iniciando descarga de AEMET...")
        self.obtener_estaciones()
        self.log("Finalizado.")