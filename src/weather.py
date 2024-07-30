import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherService:

    def __init__(self) -> None:
        self.__params = {
            "latitude": 52.3705,
            "longitude": 9.7332,
	        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
            #"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
            "timezone": "Europe/Berlin"
        }

    def get_current_weather(self):
        response: requests.Response = requests.get(API_URL, params=self.__params)
        response_json = response.json()
        return response_json        