#!/usr/bin/env python3
"""MRU Cache module
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Define a MRU cache system instance
    """
    def __init__(self):
        """Initialize an instance
        """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache

        Args:
            key: The key under which the item is stored.
            item: The item to be stored in the cache.
        """
        if not key or not item:
            return

        if key not in self.cache_data:
            # Evict the most recently used item if the cache is full
            if len(self.cache_data) >= self.MAX_ITEMS:
                discarded = self.queue.pop()
                self.cache_data.pop(discarded)
                print(f"DISCARD: {discarded}")

        # Remove the key if it already exist to maintain use order
        if key in self.queue:
            self.queue.remove(key)
        self.queue.append(key)

        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key in self.queue:
            self.queue.remove(key)
            self.queue.append(key)

        return self.cache_data.get(key)
