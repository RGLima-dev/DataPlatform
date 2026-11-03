select
    city,
    WEATHER_DATE,
    ROUND(AVG(TEMPERATURE_C),2) as avg_temperature,
    ROUND(MAX(TEMPERATURE_C),2) as max_temperature,
    ROUND(min(TEMPERATURE_C),2) as min_temperature,
    ROUND(avg(HUMIDITY_PCT),2) as avg_humidity,
    ROUND(avg(WIND_SPEED_KMH),2) as avg_wind_speed,
    ROUND(sum(PRECIPITATION_MM),2) as total_precipitation

from {{ref('stg_weather')}}

group by
    CITY,
    WEATHER_DATE