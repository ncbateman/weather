import json
import os
import time
import logging
from datetime import datetime

class CacheService:
    def __init__(self, cache_dir='/app/cache', expiry_seconds=10):
        self.cache_file = os.path.join(cache_dir, 'cache.json')
        self.expiry_seconds = expiry_seconds
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w') as file:
                json.dump({}, file)

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger('CacheService')
        self.logger.info("cache service initialized")

    def _load_cache(self):
        """ Load the cache from the file. """
        with open(self.cache_file, 'r') as file:
            return json.load(file)

    def _save_cache(self, cache):
        """ Save the cache to the file. """
        with open(self.cache_file, 'w') as file:
            json.dump(cache, file)

    def set(self, key, value):
        """ Stores the value in the cache with a timestamp. """
        cache = self._load_cache()
        cache[key] = {'value': value, 'timestamp': time.time()}
        self._save_cache(cache)
        self.logger.info(f"set cache for key: {key}")

    def get(self, key):
        """ Retrieves a value from the cache if it hasn't expired. """
        cache = self._load_cache()
        cached_item = cache.get(key)
        if not cached_item:
            self.logger.info(f"cache miss for key: {key}")
            return None

        # Check if the cache entry has expired
        if time.time() - cached_item['timestamp'] < self.expiry_seconds:
            self.logger.info(f"cache hit for key: {key}")
            return cached_item['value']
        else:
            # If the cache has expired, delete the entry and return None
            self.logger.info(f"cache expired for key: {key}")
            del cache[key]
            self._save_cache(cache)
            return None
