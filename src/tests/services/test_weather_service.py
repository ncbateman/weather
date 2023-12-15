import unittest
from unittest.mock import patch, Mock
import json
from utils.config import Config
from services.weather_service import WeatherService

class TestWeatherService(unittest.TestCase):

    def setUp(self):
        self.config = Config.get_instance()
        self.config.load_app_config(testing=True)
        self.config.load_user_credentials()
        self.weather_service = WeatherService(self.config)

    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        # Mock successful API response
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = {'current': {'temp': 15, 'pressure': 1013, 'humidity': 73, 'clouds': 90}}

        # Test get_weather method
        status_code, data = self.weather_service.get_weather(51.5074, -0.1278)
        self.assertEqual(status_code, 200)
        self.assertIn('temperature', data)
        self.assertIn('pressure', data)

    @patch('requests.get')
    def test_get_weather_api_error(self, mock_get):
        # Mock API error response
        mock_get.return_value = Mock(status_code=500)
        mock_get.return_value.json.return_value = {'message': 'Server error'}

        # Test get_weather method
        status_code, data = self.weather_service.get_weather(51.5074, -0.1278)
        self.assertEqual(status_code, 500)
        self.assertEqual(data, 'Server error')  # Check if the data is the error message


    @patch('services.weather_service.requests.get')
    def test_convert_city_to_coordinates_success(self, mock_get):
        # Mock successful geocoding API response
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = [{'lat': 51.5074, 'lon': -0.1278}]

        # Test convert_city_to_coordinates method
        lat, lon = self.weather_service.convert_city_to_coordinates("London")
        self.assertEqual(lat, 51.5074)
        self.assertEqual(lon, -0.1278)

    @patch('services.weather_service.requests.get')
    def test_convert_city_to_coordinates_failure(self, mock_get):
        # Mock failed geocoding API response
        mock_get.return_value = Mock(status_code=404)
        mock_get.return_value.json.return_value = []

        # Test convert_city_to_coordinates method
        lat, lon = self.weather_service.convert_city_to_coordinates("UnknownCity")
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    # Additional tests can be written to cover caching, error handling, etc.

if __name__ == '__main__':
    unittest.main()
