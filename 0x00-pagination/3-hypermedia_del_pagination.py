#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Deletion-resilient hypermedia data retrieval
        """
        indexed_data = self.indexed_dataset()
        total_size = len(indexed_data)

        if index is None:
            index = 0

        assert 0 <= index < total_size

        page = []

        for key, val in indexed_data.items():
            if key >= index and len(page) < page_size:
                page.append(val)
            if len(page) == page_size:
                break

        next_index = key + 1 if key < total_size - 1 else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(page),
            "data": page
        }
