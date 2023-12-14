import time

class CacheService:
    def __init__(self, expiry_seconds=3600):
        self.cache = {}
        self.expiry_seconds = expiry_seconds

    def set(self, key, value):
        """ Stores the value in the cache with a timestamp. """
        self.cache[key] = {'value': value, 'timestamp': time.time()}

    def get(self, key):
        """ Retrieves a value from the cache if it hasn't expired. """
        cached_item = self.cache.get(key)
        if not cached_item:
            print("cache miss")
            return None

        # Check if the cache entry has expired
        if time.time() - cached_item['timestamp'] < self.expiry_seconds:
            print("cache hit")
            return cached_item['value']
        else:
            # If the cache has expired, delete the entry and return None
            del self.cache[key]
            return None
