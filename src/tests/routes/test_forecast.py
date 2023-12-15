import unittest
from flask_testing import TestCase
from unittest.mock import patch
from app import create_app
from services.weather_service import WeatherService
from utils.config import Config
import os
import yaml
import base64

class TestForecast(TestCase):
    def create_app(self):
        return create_app(testing=True)

    def setUp(self):
        super(TestForecast, self).setUp()
        self.config = Config.get_instance()
        self.config.load_user_credentials()
        self.users = self.config.get_user_credentials()
        self.test_username, self.test_password = next(iter(self.users.items()))

    def get_auth_headers(self):
        credentials = f"{self.test_username}:{self.test_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {'Authorization': f'Basic {encoded_credentials}'}
        
    @patch.object(WeatherService, 'convert_city_to_coordinates')
    @patch.object(WeatherService, 'get_weather')
    def test_forecast_valid_city(self, mock_get_weather, mock_convert_city):
        auth_headers = self.get_auth_headers()
        mock_convert_city.return_value = (51.5074, -0.1278)  # Coordinates for London
        mock_get_weather.return_value = (200, {'forecast': 'sunny'})

        response = self.client.get('/forecast/London/', headers=auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sunny', response.data)

    @patch.object(WeatherService, 'convert_city_to_coordinates')
    def test_forecast_invalid_city(self, mock_convert_city):
        auth_headers = self.get_auth_headers()
        mock_convert_city.return_value = (None, None)

        response = self.client.get('/forecast/unknowncity/', headers=auth_headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'city_not_found', response.data)

    @patch.object(WeatherService, 'convert_city_to_coordinates')
    def test_forecast_invalid_date_format(self, mock_convert_city):
        auth_headers = self.get_auth_headers()
        mock_convert_city.return_value = (51.5074, -0.1278)

        response = self.client.get('/forecast/London/?at=invalid-date', headers=auth_headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'invalid_date_format', response.data)

if __name__ == '__main__':
    unittest.main()
