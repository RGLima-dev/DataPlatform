import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
import boto3
import os

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
    s3 = boto3.client("s3")
    bucket_name = os.environ["S3_BUCKET_NAME"]

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
            data["city"] = citie_data['city']

        output_dir = Path(f"/opt/spark/data/raw/weather/{citie_data['city']}")
        output_dir.mkdir(parents=True, exist_ok=True)

        s3_key = (
            f"raw/weather/"
            f"{citie_data['city']}/"
            f"{citie_data['city']}_{timestamp}.json"
        )

        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(data,ensure_ascii=False,indent=4),
            ContentType="application/json",
        )

        print(f"Written to s3://{bucket_name}/{s3_key}")