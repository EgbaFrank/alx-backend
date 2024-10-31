#!/usr/bin/env python3
"""LFU Cache module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Define a LFU cache system instance
    """
    def __init__(self):
        """Initialize an instance
        """
        super().__init__()
        self.usage_frequency = {}

    def put(self, key, item):
        """ Add an item in the cache

        Args:
            key: The key under which the item is stored.
            item: The item to be stored in the cache.
        """
        if not key or not item:
            return

        if key not in self.cache_data:
            # Evict the least frequently used item if the cache is full
            if len(self.cache_data) >= self.MAX_ITEMS:
                least_used_key = min(
                    self.usage_frequency,
                    key=lambda k: self.usage_frequency[k][1]
                )
                self.cache_data.pop(least_used_key)
                self.usage_frequency.pop(least_used_key)
                print(f"DISCARD: {least_used_key}")

        current_frequency = (
            self.usage_frequency[key][1] + 1
            if key in self.usage_frequency
            else 1
        )
        self.cache_data[key] = item
        self.usage_frequency[key] = (item, current_frequency)

    def get(self, key):
        """ Get an item by key
        """
        if key in self.usage_frequency:
            # Increment the frequency count upon access
            item, frequency = self.usage_frequency[key]
            self.usage_frequency[key] = (item, frequency + 1)

        return self.cache_data.get(key)
