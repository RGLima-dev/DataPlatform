select
    city,
    date(weather_timestamp) as weather_date,
    avg(temperature_c) as avg_temperature,
    max(temperature_c) as max_temperature,
    min(temperature_c) as min_temperature,
    avg(humidity_pct) as avg_humidity,
    avg(wind_speed_kmh) as avg_wind_speed,
    sum(precipitation_mm) as total_precipitation

from {{ source('weather', 'silver_weather') }}

group by
    city,
    date(weather_timestamp)