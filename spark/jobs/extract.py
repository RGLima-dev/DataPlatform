import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
import time


BASE_URL = "https://api.open-meteo.com/v1/forecast"

LATITUDE = -21.79
LONGITUDE = -48.18

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ],
    "timezone": "America/Sao_Paulo",
}

query_string = urllib.parse.urlencode(
    params,
    doseq=True,
)

url = f"{BASE_URL}?{query_string}"

print("Calling API...")
print(url)

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))

print("API request successful.")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_dir = Path("/opt/spark/data/raw/weather")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / f"araraquara_{timestamp}.json"

with open(output_file, "w") as file:
    json.dump(data, file, indent=4)

print(f"Raw file written to: {output_file}")