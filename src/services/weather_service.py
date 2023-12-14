import requests

class WeatherService:
    def __init__(self, config):
        self.api_key = config['API_KEY']
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, city):
        """
        Fetches weather data for a given city.
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # or 'imperial' for Fahrenheit
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return self.process_response(response.json())
        else:
            # Instead of raising an error, return the error message
            error_message = response.json().get('message', 'Unknown error')
            return {'error': error_message}

    def process_response(self, data):
        """
        Processes the API response and extracts relevant weather data.
        """
        weather_data = {
            'clouds': data['weather'][0]['description'],
            'humidity': f"{data['main']['humidity']}%",
            'pressure': f"{data['main']['pressure']} hPa",
            'temperature': f"{data['main']['temp']}C"
        }
        return weather_data
