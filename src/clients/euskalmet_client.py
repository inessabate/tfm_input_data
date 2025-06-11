import requests
import json
import re
from pathlib import Path
from src.clients.base_client import BaseClient

class EuskalmetClient(BaseClient):
    def __init__(self):
        super().__init__("euskalmet")

        self.url_stations = (
            "https://opendata.euskadi.eus/contenidos/"
            "ds_meteorologicos/estaciones_meteorologicas/opendata/estaciones-padding.geojson"
        )

        self.stations_path = Path(__file__).resolve().parent.parent.parent / "data" / "raw" / self.name.lower() / f"{self.name.upper()}_stations.json"
        self.download_dir = self.output_dir / "xml_observations"
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def get_stations(self):
        try:
            response = requests.get(self.url_stations)
            response.raise_for_status()
            raw_text = response.text

            match = re.search(r'jsonCallback\(\s*(\{.*\})\s*\)', raw_text, flags=re.DOTALL)
            if match:
                json_text = match.group(1)
                data = json.loads(json_text)
                self.save_json(f"{self.name.upper()}_stations", data, include_date=False)
            else:
                self.log("Could not extract JSON from jsonCallback(...)")
        except Exception as e:
            self.log(f"Error retrieving stations: {e}")

    def get_station_codes(self) -> list[str]:
        if not self.stations_path.exists():
            raise FileNotFoundError(f"Station file not found: {self.stations_path}")

        with open(self.stations_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            feature["properties"]["codigo"].upper().strip()
            for feature in data.get("features", [])
            if feature.get("properties", {}).get("codigo")
        ]

    def generate_monthly_xml_urls(self, year: int = 2024) -> list[tuple[str, str]]:
        """Generate a list of (url, filename) tuples for valid XML files."""
        base_url = (
            "https://opendata.euskadi.eus/contenidos/ds_meteorologicos/"
            "met_stations_ds_{year}/opendata/{year}/{station}/{station}_{year}_{month}.xml"
        )
        station_codes = self.get_station_codes()
        urls = []

        for code in station_codes:
            for month in range(1, 13):
                url = base_url.format(year=year, station=code, month=month)
                filename = f"{code}_{year}_{month}.xml"
                urls.append((url, filename))

        return urls

    def get_daily_observations(self):
        """Verify .xml URLs, download valid ones, and store them locally."""
        try:
            urls = self.generate_monthly_xml_urls()
            valid_urls = []

            self.log("Checking and downloading available .xml observation files...")

            for url, filename in urls:
                try:
                    head = requests.head(url)
                    if head.status_code == 200:
                        valid_urls.append(url)

                        # Download and save
                        content = requests.get(url).content
                        save_path = self.download_dir / filename
                        with open(save_path, "wb") as f:
                            f.write(content)
                        self.log(f"Downloaded: {filename}")
                    else:
                        self.log(f"Skipped (not found): {filename}")
                except Exception as e:
                    self.log(f"Error checking/downloading {url}: {e}")

            self.save_json("euskalmet_valid_xml_urls", valid_urls, include_date=False)
            self.log(f"Total XML files downloaded: {len(valid_urls)}")

        except Exception as e:
            self.log(f"Error generating or downloading observation files: {e}")

    def ejecutar(self):
        print()
        self.log(f"Starting {self.name.upper()} download...")
        self.get_stations()
        self.get_daily_observations()
        self.log(f"Finished data retrieval from {self.name.upper()}.")