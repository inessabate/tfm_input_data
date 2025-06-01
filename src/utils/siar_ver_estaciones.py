import requests
from dotenv import load_dotenv
import os

# Cargar la clave API
load_dotenv()
api_key = os.getenv("API_KEY_SIAR")

# Verificar que se ha cargado la clave
if not api_key:
    raise ValueError("Clave API no cargada. Revisa tu archivo .env.")

# Hacer petición a la API para obtener estaciones autorizadas
url = "https://servicio.mapama.gob.es/apisiar/API/v1/Info/Estaciones"
params = {"ClaveAPI": api_key}

response = requests.get(url, params=params)

# Mostrar resultados
if response.status_code == 200:
    estaciones = response.json().get("Datos", [])
    for est in estaciones:
        print(est)
        #print(f"{est['Id']}: {est['Descripcion']}")
else:
    print(f"Error {response.status_code}: {response.text}")