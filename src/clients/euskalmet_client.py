
from src.clients.base_client import BaseClient

import requests
import re
import json

class EuskalmetClient(BaseClient):
    def __init__(self):
        super().__init__("euskalmet")

        self.url_estaciones = "https://opendata.euskadi.eus/contenidos/ds_meteorologicos/estaciones_meteorologicas/opendata/estaciones-padding.geojson"
        #self.url_mediciones = "https://opendata.euskadi.eus/contenidos_recurso/opendata/meteorologia_lecturas/opendata/.json"

    def descargar_estaciones(self):
        try:
            response = requests.get(self.url_estaciones)
            response.raise_for_status()
            raw_text = response.text

            match = re.search(r'jsonCallback\(\s*(\{.*\})\s*\)', raw_text, flags=re.DOTALL)
            if match:
                json_text = match.group(1)
                data = json.loads(json_text)
                self.save_json("estaciones_euskalmet", data, include_date=False)
            else:

                self.log("❌ Could not extract JSON from jsonCallback(...)")
        except Exception as e:
            self.log(f"Error in retrieving stations: {e}")

    def descargar_mediciones(self):
        """
        Download measurements from Euskalmet and save them as JSON.
        The URL for measurements is not provided in the original code, so this method
        is a placeholder. You may need to adjust the URL based on actual API documentation.
        """
        try:
            response = requests.get(self.url_mediciones)
            response.raise_for_status()
            self.save_json("mediciones_euskalmet", response.json(), include_date=True)
        except Exception as e:
            self.log(f"Error al descargar mediciones: {e}")

    def ejecutar(self):
        """
        Execute the Euskalmet client to download stations and measurements.
        """
        self.log(f"Starting {self.name.upper()} download...")
        self.descargar_estaciones()
        self.descargar_mediciones()
        self.log(f"Finished data retrieval from {self.name.upper()}.")
