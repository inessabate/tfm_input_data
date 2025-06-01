from src.clients.base_client import BaseClient

import requests
import os
from dotenv import load_dotenv

class SiarClient(BaseClient):
    def __init__(self, estaciones, fecha_inicial, fecha_final):
        load_dotenv()
        api_key = os.getenv("API_KEY_SIAR")
        if not api_key:
            raise ValueError("No se pudo cargar API_KEY_SIAR desde .env.")
        super().__init__("siar")
        self.api_key = api_key
        self.estaciones = estaciones
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
                self.log(f"Consultando estación {est}")
                datos = self.fetch_datos_estacion(est)
                if datos:
                    self.guardar_json(f"mediciones_{est}", datos)
                else:
                    self.log(f"No se encontraron datos para {est}")
            except Exception as e:
                self.log(f"❌ Error con {est}: {e}")

    def ejecutar(self):
        self.log("Iniciando descarga de SIAR...")
        self.descargar_mediciones()
        self.log("Finalizado.")