import requests
import logging
from .cache_service import CacheService

class WeatherService:
    def __init__(self, config):
        # Initialize the WeatherService class with configuration settings.
        # config: A dictionary containing configuration settings like API key.

        # Extract the API key and base URL for the OpenWeatherMap API.
        self.api_key = config['API_KEY']
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"

        # Initialize the CacheService to cache weather data.
        self.cache = CacheService()

        # Set up logging with a specific format and level.
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger('WeatherService')
        self.logger.info("Weather service initialized")

    def get_weather(self, lat, lon, timestamp=None):
        """
        Fetches weather data for given coordinates. If a timestamp is provided,
        fetches historical weather data for that time, otherwise fetches current weather data.
        """
        # Create a unique cache key based on latitude, longitude, and timestamp.
        cache_key = f"{lat},{lon},{timestamp}"

        # Try to retrieve the response from cache first.
        cached_response = self.cache.get(cache_key)
        if cached_response:
            # If cached data is available, return it without making an API call.
            return 200, cached_response

        # Prepare the parameters for the API request.
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  # Set units to metric.
            'exclude': 'minutely,daily,alerts'  # Exclude unnecessary data.
        }

        # If a timestamp is provided, fetch historical data; otherwise, fetch current data.
        if timestamp:
            endpoint = self.base_url + "/timemachine"
            params['dt'] = timestamp
        else:
            endpoint = self.base_url

        # Prepare and log the full request URL.
        prepared_request = requests.Request('GET', endpoint, params=params).prepare()
        full_url = prepared_request.url
        self.logger.info(f"Request URL: {full_url}")

        # Make the API request.
        response = requests.get(full_url)
        if response.status_code == 200:
            # Process the response if the status code is 200 (OK).
            weather_data = self.process_response(response.json())
            # Store the processed data in cache.
            self.cache.set(cache_key, weather_data)
            return response.status_code, weather_data
        else:
            # Log the error if the API response is not successful.
            self.logger.error(f"API error: {response.status_code}, {response.json().get('message', 'Unknown error')}")
            return response.status_code, response.json().get('message', 'Unknown error')

    def process_response(self, data):
        """
        Processes the API response and extracts relevant weather data.
        """
        # Check and extract relevant data from the API response.
        if 'data' in data:
            weather_data_point = data['data'][0]
        elif 'current' in data:
            weather_data_point = data['current']
        else:
            # Log and return an error if the data format is not as expected.
            self.logger.error("Invalid data format in response")
            return {'error': 'Invalid data format'}

        # Extract and format specific weather details from the data point.
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
        # Prepare the URL and parameters for the geocoding API request.
        geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': city_name,
            'limit': 1,  # Limit the response to one result.
            'appid': self.api_key
        }

        # Make the geocoding API request.
        response = requests.get(geocoding_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Return the latitude and longitude if the city is found.
                return data[0]['lat'], data[0]['lon']
            else:
                # Log an error if the city is not found in the response.
                self.logger.error(f"City not found: {city_name}")
                return None, None
        else:
            # Log and raise an error if the geocoding API response is not successful.
            self.logger.error(f"Geocoding API error: {response.status_code}")
            raise Exception(f"Geocoding API error: {response.status_code}")