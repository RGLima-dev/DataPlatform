import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_cities_cordinates(city_name:list[str]):
    cities = []
    for citie in city_name:
        params = {
            "name": citie,
            "count": 10,
            "language": "en",
            "format": "json",
        }

        query_string = urllib.parse.urlencode(params,doseq=True)
        url = f"{GEOCODING_URL}?{query_string}"

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))


        results = data.get("results",[])
        result = results[0]

        cities.append({
            "city": result["name"],
            "latitude": result["latitude"],
            "longitude": result["longitude"],
        })

    return cities


def get_weather(city_data:list[dict]):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for citie_data in city_data:
        params = {
        "latitude": citie_data["latitude"],
        "longitude": citie_data["longitude"],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
        ],
        "timezone": "America/Sao_Paulo",
}   
        query_string = urllib.parse.urlencode(params,doseq=True)
        url = f"{FORECAST_URL}?{query_string}"

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))

        output_dir = Path(f"/opt/spark/data/raw/weather/{citie_data['city']}")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{citie_data['city']}_{timestamp}.json"
        print(output_file)
        print(data)

        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Raw file written to: {output_file}")