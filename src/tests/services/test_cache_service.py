import unittest
from unittest.mock import patch
import os
import json
from services.cache_service import CacheService
import time

class TestCacheService(unittest.TestCase):
    def setUp(self):
        # Use a temporary directory for testing the cache
        self.temp_cache_dir = '/tmp/test_cache'
        os.makedirs(self.temp_cache_dir, exist_ok=True)
        self.cache_service = CacheService(cache_dir=self.temp_cache_dir, expiry_seconds=2)

    def tearDown(self):
        # Clean up the temporary directory after tests
        if os.path.exists(self.temp_cache_dir):
            for file in os.listdir(self.temp_cache_dir):
                os.remove(os.path.join(self.temp_cache_dir, file))
            os.rmdir(self.temp_cache_dir)

    def test_set_and_get_cache(self):
        # Test setting and retrieving a value from the cache
        self.cache_service.set('test_key', 'test_value')
        value = self.cache_service.get('test_key')
        self.assertEqual(value, 'test_value', "Cache should return the correct value")

    def test_cache_expiry(self):
        # Test that values expire from the cache as expected
        self.cache_service.set('test_key', 'test_value')
        time.sleep(3)  # Wait longer than the expiry time
        value = self.cache_service.get('test_key')
        self.assertIsNone(value, "Expired cache values should return None")

    def test_nonexistent_key(self):
        # Test retrieval of a key that was never set
        value = self.cache_service.get('nonexistent_key')
        self.assertIsNone(value, "Nonexistent keys should return None")

    def test_overwrite_existing_key(self):
        # Test that setting a new value overwrites the existing value
        self.cache_service.set('test_key', 'initial_value')
        self.cache_service.set('test_key', 'new_value')
        value = self.cache_service.get('test_key')
        self.assertEqual(value, 'new_value', "Cache should overwrite existing values")

    def test_cache_persistence(self):
        # Test that cache values persist between service instances
        self.cache_service.set('persistent_key', 'value')
        new_cache_service = CacheService(cache_dir=self.temp_cache_dir, expiry_seconds=2)
        value = new_cache_service.get('persistent_key')
        self.assertEqual(value, 'value', "Cache values should persist between instances")

    def test_cache_file_structure(self):
        # Test the structure of the cache file
        self.cache_service.set('key1', 'value1')
        with open(os.path.join(self.temp_cache_dir, 'cache.json'), 'r') as file:
            cache_content = json.load(file)
        self.assertIn('key1', cache_content)
        self.assertIsInstance(cache_content['key1'], dict)
        self.assertIn('value', cache_content['key1'])
        self.assertIn('timestamp', cache_content['key1'])

    # Additional tests can be added as needed

if __name__ == '__main__':
    unittest.main()
