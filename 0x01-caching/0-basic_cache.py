#!/usr/bin/env python3
"""Basic Cache module
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Define a basic cache instance
    """
    def __init__(self):
        """Initialize an instance
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key)
