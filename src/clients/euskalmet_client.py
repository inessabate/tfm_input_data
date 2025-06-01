
from src.clients.base_client import BaseClient

import requests
import re
import json

class EuskalmetClient(BaseClient):
    def __init__(self):
        super().__init__("euskalmet")

        self.url_estaciones = "https://opendata.euskadi.eus/contenidos/ds_meteorologicos/estaciones_meteorologicas/opendata/estaciones-padding.geojson"
        self.url_mediciones = "https://opendata.euskadi.eus/contenidos_recurso/opendata/meteorologia_lecturas/opendata/.json"

    def descargar_estaciones(self):
        try:
            response = requests.get(self.url_estaciones)
            response.raise_for_status()
            raw_text = response.text

            match = re.search(r'jsonCallback\(\s*(\{.*\})\s*\)', raw_text, flags=re.DOTALL)
            if match:
                json_text = match.group(1)
                data = json.loads(json_text)
                self.guardar_json("estaciones_euskalmet", data)
            else:
                self.log("❌ No se pudo extraer JSON desde jsonCallback(...)")
        except Exception as e:
            self.log(f"Error al descargar estaciones: {e}")
    def descargar_mediciones(self):
        try:
            response = requests.get(self.url_mediciones)
            response.raise_for_status()
            self.guardar_json("mediciones_euskalmet", response.json())
        except Exception as e:
            self.log(f"Error al descargar mediciones: {e}")

    def ejecutar(self):
        self.log("Iniciando descarga de Euskalmet...")
        self.descargar_estaciones()
        self.descargar_mediciones()
        self.log("Finalizado.")
