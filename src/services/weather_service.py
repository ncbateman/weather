import requests
import logging
from .cache_service import CacheService

class WeatherService:
    def __init__(self, config):
        self.api_key = config['API_KEY']
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.cache = CacheService()

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger('WeatherService')
        self.logger.info("weather service initialized")

    def get_weather(self, lat, lon, timestamp=None):
        """
        Fetches weather data for given coordinates. If a timestamp is provided,
        fetches historical weather data for that time, otherwise fetches current weather data.
        """
        cache_key = f"{lat},{lon},{timestamp}"
        cached_response = self.cache.get(cache_key)
        if cached_response:
            return 200, cached_response

        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'exclude': 'minutely,daily,alerts'
        }

        if timestamp:
            endpoint = self.base_url + "/timemachine"
            params['dt'] = timestamp
        else:
            endpoint = self.base_url

        prepared_request = requests.Request('GET', endpoint, params=params).prepare()
        full_url = prepared_request.url
        self.logger.info(f"request URL: {full_url}")

        response = requests.get(full_url)
        if response.status_code == 200:
            weather_data = self.process_response(response.json())
            self.cache.set(cache_key, weather_data)
            return response.status_code, weather_data
        else:
            self.logger.error(f"API error: {response.status_code}, {response.json().get('message', 'Unknown error')}")
            return response.status_code, response.json().get('message', 'Unknown error')

    def process_response(self, data):
        """
        Processes the API response and extracts relevant weather data.
        """
        if 'data' in data:
            weather_data_point = data['data'][0]
        elif 'current' in data:
            weather_data_point = data['current']
        else:
            self.logger.error("invalid data format in response")
            return {'error': 'Invalid data format'}

        weather_data = {
            'temperature': f"{weather_data_point.get('temp', 'N/A')}°C",
            'pressure': f"{weather_data_point.get('pressure', 'N/A')} hPa",
            'humidity': f"{weather_data_point.get('humidity', 'N/A')}%",
            'clouds': f"{weather_data_point.get('clouds', 'N/A')}%"
        }

        return weather_data

    def convert_city_to_coordinates(self, city_name):
        """
        Converts a city name to latitude and longitude using the OpenWeatherMap Geocoding API.
        """
        geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': city_name,
            'limit': 1,
            'appid': self.api_key
        }
        response = requests.get(geocoding_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                self.logger.error(f"City not found: {city_name}")
                return None, None
        else:
            self.logger.error(f"Geocoding API error: {response.status_code}")
            raise Exception(f"Geocoding API error: {response.status_code}")
