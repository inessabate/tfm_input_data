from src.clients.base_client import BaseClient

import requests
from dotenv import load_dotenv
import os

class MeteoGaliciaClient(BaseClient):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("API_KEY_METEOGALICIA")
        if not api_key:
            raise ValueError("API_KEY_METEOGALICIA no está definida en .env")
        super().__init__("meteogalicia")
        self.api_key = api_key
        self.base_url = "https://servizos.meteogalicia.gal/apiv4"

    def fetch_localidades(self):
        localidades = []
        for letra in 'abcdefghijklmnopqrstuvwxyz':
            url = f"{self.base_url}/findPlaces?location={letra}&API_KEY={self.api_key}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    features = data.get("features", [])
                    if features:
                        localidades.extend(features)
                    else:
                        self.log(f"Sin resultados para letra '{letra}'")
                else:
                    self.log(f"Respuesta no exitosa para letra '{letra}': {response.status_code}")
            except Exception as e:
                self.log(f"Error con letra '{letra}': {e}")
        return localidades

    def descargar_estaciones(self):
        localidades = self.fetch_localidades()
        self.guardar_json("localidades_meteogalicia", localidades)

    def ejecutar(self):
        self.log("Iniciando descarga de localidades MeteoGalicia...")
        self.descargar_estaciones()
        self.log("Finalizado.")
