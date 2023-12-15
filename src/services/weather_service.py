import logging
import requests
from utils.config import Config
from .cache_service import CacheService
from utils.config import Config

class WeatherService:
    def __init__(self, config):
        """
        Initialize the WeatherService class using settings from the Config utility class.

        This initialization sets up the WeatherService with API keys and base URLs 
        required for interacting with the OpenWeatherMap API. It also initializes a 
        CacheService for caching weather data and sets up logging.
        """

        config = Config.get_instance().get_app_config()

        # Extract the API key, base URL, and Geocoding URL for the OpenWeatherMap API.
        # Retrieve configuration settings using attribute access
        self.api_key = config['API_KEY']
        self.base_url = config['BASE_URL']
        self.geocoding_url = config['GEOCODING_URL']

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

        Args:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.
            timestamp (int, optional): Unix timestamp for historical data. Defaults to None.

        Returns:
            tuple: HTTP status code and the weather data or error message.
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

        # Determine the appropriate endpoint based on the presence of a timestamp.
        endpoint = self.base_url + "/timemachine" if timestamp else self.base_url
        if timestamp:
            params['dt'] = timestamp

        # Prepare and log the full request URL.
        prepared_request = requests.Request('GET', endpoint, params=params).prepare()
        self.logger.info(f"Request URL: {prepared_request.url}")

        # Make the API request and handle the response.
        response = requests.get(prepared_request.url)
        if response.status_code == 200:
            # Process and cache the response if successful.
            weather_data = self.process_response(response.json())
            self.cache.set(cache_key, weather_data)
            return response.status_code, weather_data
        else:
            # Log the error for unsuccessful API responses.
            self.logger.error(f"API error: {response.status_code}, {response.json().get('message', 'Unknown error')}")
            return response.status_code, response.json().get('message', 'Unknown error')

    def process_response(self, data):
        """
        Processes the API response and extracts relevant weather data.

        Args:
            data (dict): The raw data received from the API.

        Returns:
            dict: Processed weather data.
        """
        # Extract relevant data based on the structure of the response.
        if 'data' in data:
            weather_data_point = data['data'][0]
        elif 'current' in data:
            weather_data_point = data['current']
        else:
            self.logger.error("Invalid data format in response")
            return {'error': 'Invalid data format'}

        # Format the extracted weather details.
        return {
            'temperature': f"{weather_data_point.get('temp', 'N/A')}C",
            'pressure': f"{weather_data_point.get('pressure', 'N/A')}hPa",
            'humidity': f"{weather_data_point.get('humidity', 'N/A')}%",
            'clouds': f"{weather_data_point.get('clouds', 'N/A')}%"
        }

    def convert_city_to_coordinates(self, city_name):
        """
        Converts a city name to latitude and longitude using the OpenWeatherMap Geocoding API.

        Args:
            city_name (str): The name of the city to convert.

        Returns:
            tuple: Latitude and longitude of the city, or None, None if not found or in case of an error.
        """
        # Prepare the parameters for the geocoding API request.
        params = {'q': city_name, 'limit': 1, 'appid': self.api_key}

        # Make the geocoding API request.
        response = requests.get(self.geocoding_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                self.logger.error(f"City not found: {city_name}")
                return None, None
        else:
            self.logger.error(f"Geocoding API error: {response.status_code}")
            return None, None
