import requests

class WeatherService:
    def __init__(self, config):
        self.api_key = config['API_KEY']
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"

    def get_weather(self, lat, lon, timestamp=None):
        """
        Fetches weather data for given coordinates. If a timestamp is provided,
        fetches historical weather data for that time, otherwise fetches current weather data.
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'exclude': 'minutely,daily,alerts'
        }

        # If timestamp is provided, use the timemachine endpoint
        if timestamp:
            endpoint = self.base_url + "/timemachine"
            params['dt'] = timestamp
        else:
            endpoint = self.base_url

        # Prepare the request without sending it to get the full URL
        prepared_request = requests.Request('GET', endpoint, params=params).prepare()
        full_url = prepared_request.url

        # Print the full URL
        print("Request URL:", full_url)

        response = requests.get(full_url)
        if response.status_code == 200:
            return response.status_code, self.process_response(response.json())
        else:
            return response.status_code, response.json().get('message', 'Unknown error')


    def process_response(self, data):
        """
        Processes the API response and extracts relevant weather data.
        """

        # Check if response is for a specific timestamp
        if 'data' in data:
            weather_data_point = data['data'][0]  # Historical data
        elif 'current' in data:
            weather_data_point = data['current']  # Current data
        else:
            return {'error': 'Invalid data format'}

        weather_data = {
            'temperature': f"{weather_data_point.get('temp', 'N/A')}°C",
            'pressure': f"{weather_data_point.get('pressure', 'N/A')} hPa",
            'humidity': f"{weather_data_point.get('humidity', 'N/A')}%",
            'clouds': f"{weather_data_point.get('clouds', 'N/A')}%"
        }

        # Add rain information if available
        if 'rain' in weather_data_point:
            weather_data['rain'] = f"{weather_data_point['rain'].get('1h', 'N/A')} mm"

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
                return None, None
        else:
            raise Exception(f"Geocoding API error: {response.status_code}")
