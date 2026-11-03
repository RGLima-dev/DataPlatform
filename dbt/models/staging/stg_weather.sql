SELECT 
    city AS CITY,
    latitude AS LATITUDE,
    longitude AS LONGITUDE,
    date(weather_timestamp) AS WEATHER_DATE,
    CAST(ROUND(temperature_c,2) AS decimal(10,2)) AS TEMPERATURE_C,
    humidity_pct AS HUMIDITY_PCT,
    CAST(ROUND(precipitation_mm,2) AS decimal(10,2)) AS PRECIPITATION_MM,
    CAST(ROUND(wind_speed_kmh,2) AS decimal(10,2)) AS WIND_SPEED_KMH,
    ingestion_timestamp AS INGESTION_TIMESTAMP,
    source_file AS SOURCE_FILE
FROM {{source('weather','silver_weather')}}