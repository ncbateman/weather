import unittest
from flask_testing import TestCase
from app import create_app
import json

class TestPingRoute(TestCase):
    def create_app(self):
        # Create an instance of the app with the testing configuration
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

if __name__ == '__main__':
    unittest.main()
