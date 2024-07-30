import json
import logging
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherService:

    def __init__(self) -> None:
        self.__params = {
            "latitude": 52.3705,
            "longitude": 9.7332,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "daylight_duration", "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"],
            "timezone": "Europe/Berlin",
            "forecast_days": 3
        }

    def get_current_weather(self):
        response: requests.Response = requests.get(API_URL, params=self.__params)
        response_json = response.json()
        logging.debug(json.dumps(response_json, indent=2))
        return response_json        