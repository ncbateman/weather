import json
import os
import time
import logging
from datetime import datetime

class CacheService:
    def __init__(self, cache_dir='/app/cache', expiry_seconds=10):
        # Initialize the CacheService class with default cache directory and expiry time.
        # cache_dir: Directory where the cache file will be stored.
        # expiry_seconds: Time in seconds after which a cache entry is considered expired.

        # Construct the path to the cache file.
        self.cache_file = os.path.join(cache_dir, 'cache.json')
        
        # Store the expiry duration for cache items.
        self.expiry_seconds = expiry_seconds

        # Create the cache directory if it does not exist.
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Create an empty cache file if it does not exist.
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w') as file:
                json.dump({}, file)

        # Set up logging with a specific format and level.
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger('CacheService')
        self.logger.info("Cache service initialized")

    def _load_cache(self):
        """ Load the cache from the file. """
        # Open the cache file and load its content as a JSON object.
        with open(self.cache_file, 'r') as file:
            return json.load(file)

    def _save_cache(self, cache):
        """ Save the cache to the file. """
        # Write the cache content to the file as a JSON object.
        with open(self.cache_file, 'w') as file:
            json.dump(cache, file)

    def set(self, key, value):
        """ Stores the value in the cache with a timestamp. """
        # Set a value in the cache with the associated key.
        # key: The key under which the value will be stored.
        # value: The value to be stored in the cache.

        # Load the current state of the cache.
        cache = self._load_cache()
        
        # Add or update the value in the cache along with the current timestamp.
        cache[key] = {'value': value, 'timestamp': time.time()}
        
        # Save the updated cache back to the file.
        self._save_cache(cache)
        
        # Log the action of setting a cache value.
        self.logger.info(f"Set cache for key: {key}")

    def get(self, key):
        """ Retrieves a value from the cache if it hasn't expired. """
        # Retrieve a value from the cache if it's still valid.
        # key: The key whose value needs to be retrieved.

        # Load the cache.
        cache = self._load_cache()
        
        # Fetch the item from cache.
        cached_item = cache.get(key)
        
        # If the item is not found in cache, log and return None.
        if not cached_item:
            self.logger.info(f"Cache miss for key: {key}")
            return None

        # Check if the cache entry has expired.
        if time.time() - cached_item['timestamp'] < self.expiry_seconds:
            # If not expired, log a cache hit and return the value.
            self.logger.info(f"Cache hit for key: {key}")
            return cached_item['value']
        else:
            # If expired, delete the entry, save the cache, log, and return None.
            self.logger.info(f"Cache expired for key: {key}")
            del cache[key]
            self._save_cache(cache)
            return None
