from .common_extraction_functions import (
    get_cities_cordinates,
    get_weather
)

from commons.cities import city_name

cities = city_name()
evaluated_cities = get_cities_cordinates(cities)
get_weather(evaluated_cities)
