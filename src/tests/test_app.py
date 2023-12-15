import unittest
from flask_testing import TestCase
from unittest.mock import patch
import json
from app import create_app
from services.weather_service import WeatherService

class TestApp(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        return create_app(testing=True)

    def test_ping_route(self):
        """
        Test the /ping route to ensure it returns the correct response.
        """
        response = self.client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = json.loads(response.data.decode('utf-8'))
        
        # Assert the values
        self.assertEqual(data['name'], 'weatherservice')
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['version'], '1.0.0')

    def test_404_error_handler(self):
        """
        Test the 404 error handler.
        """
        response = self.client.get('/nonexistentroute/')
        self.assertEqual(response.status_code, 404)

        # Parse the JSON response
        data = json.loads(response.data.decode('utf-8'))
        
        # Assert the values
        self.assertEqual(data['error'], 'Not found')
        self.assertEqual(data['error_code'], 'not_found')

    def test_app_config(self):
        """
        Test the application's configuration settings.
        """
        self.assertTrue(self.app.config['TESTING'])
        self.assertEqual(self.app.config['API_KEY'], 'test_api_key')  # Assert that the API key is as expected

    @patch.object(WeatherService, 'convert_city_to_coordinates')
    @patch.object(WeatherService, 'get_weather')
    def test_forecast_route(self, mock_get_weather, mock_convert_city):
        """
        Test the /forecast route with a valid city.
        """
        mock_convert_city.return_value = (51.5074, -0.1278)  # Coordinates for London
        mock_get_weather.return_value = (200, {'forecast': 'sunny'})

        response = self.client.get('/forecast/London/')
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        data = json.loads(response.data.decode('utf-8'))
        
        # Assert the forecast data
        self.assertIn('forecast', data)
        self.assertEqual(data['forecast'], 'sunny')

    @patch.object(WeatherService, 'convert_city_to_coordinates')
    def test_forecast_invalid_city(self, mock_convert_city):
        """
        Test the /forecast route with an invalid city.
        """
        mock_convert_city.return_value = (None, None)

        response = self.client.get('/forecast/unknowncity/')
        self.assertEqual(response.status_code, 404)

        # Parse the JSON response
        data = json.loads(response.data.decode('utf-8'))
        
        # Assert the error response
        self.assertEqual(data['error'], "Cannot find city 'unknowncity'")
        self.assertEqual(data['error_code'], 'city_not_found')

    @patch.object(WeatherService, 'get_weather')
    def test_500_error_handler(self, mock_get_weather):
        """
        Test the 500 error handler.
        """
        # Configure the mock to raise an exception
        mock_get_weather.side_effect = Exception("Test exception")

        # Make a request that would normally call the mocked method
        response = self.client.get('/forecast/somecity/')

        # Assert that a 500 status code is returned
        self.assertEqual(response.status_code, 500)

        # Parse the JSON response
        data = json.loads(response.data.decode('utf-8'))

        # Assert the values in the response
        self.assertEqual(data['error'], 'Something went wrong')
        self.assertEqual(data['error_code'], 'internal_server_error')

if __name__ == '__main__':
    unittest.main()
