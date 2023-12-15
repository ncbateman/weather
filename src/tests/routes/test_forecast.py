import unittest
from flask_testing import TestCase
from unittest.mock import patch
from app import create_app
from services.weather_service import WeatherService

class TestForecast(TestCase):
    def create_app(self):
        # Create an instance of the app with the testing configuration
        return create_app(testing=True)
        

    @patch.object(WeatherService, 'convert_city_to_coordinates')
    @patch.object(WeatherService, 'get_weather')
    def test_forecast_valid_city(self, mock_get_weather, mock_convert_city):
        mock_convert_city.return_value = (51.5074, -0.1278)  # Coordinates for London
        mock_get_weather.return_value = (200, {'forecast': 'sunny'})

        response = self.client.get('/forecast/London/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sunny', response.data)

    @patch.object(WeatherService, 'convert_city_to_coordinates')
    def test_forecast_invalid_city(self, mock_convert_city):
        mock_convert_city.return_value = (None, None)

        response = self.client.get('/forecast/unknowncity/')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'city_not_found', response.data)

    @patch.object(WeatherService, 'convert_city_to_coordinates')
    def test_forecast_invalid_date_format(self, mock_convert_city):
        mock_convert_city.return_value = (51.5074, -0.1278)

        response = self.client.get('/forecast/London/?at=invalid-date')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'invalid_date_format', response.data)

# Add more tests as necessary...

if __name__ == '__main__':
    unittest.main()
