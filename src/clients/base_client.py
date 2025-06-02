
import json
from pathlib import Path
from datetime import datetime

class BaseClient:
    def __init__(self, nombre_fuente: str):
        self.nombre = nombre_fuente.upper()

        # Ruta relativa a la raíz del proyecto (fuera de src/)
        self.output_dir = Path(__file__).resolve().parent.parent.parent / "data" / "raw" / nombre_fuente.lower()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.fecha_hoy = datetime.today().strftime("%Y-%m-%d")

    def guardar_json(self, nombre_archivo: str, contenido: dict | list):
        """Guarda contenido JSON en un archivo nombrado con la fecha de hoy."""
        filename = f"{nombre_archivo}_{self.fecha_hoy}.json"
        path = self.output_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(contenido, f, indent=2, ensure_ascii=False)
        print(f"📁 [{self.nombre}] Guardado: {path}")

    def log(self, mensaje: str):
        """Log formateado uniforme por fuente."""
        print(f"[{self.nombre}] {mensaje}")



