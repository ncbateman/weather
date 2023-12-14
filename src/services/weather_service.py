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
            return response.status_code, self.process_response(response.json())
        else:
            # Pass through the status code and error message
            return response.status_code, response.json().get('message', 'Unknown error')

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
