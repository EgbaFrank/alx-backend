#!/usr/bin/env python3
"""
Contains a simple paginator
"""
import csv
from typing import Tuple, List, Any, Union, Dict


def index_range(page: int, page_size: int) -> Tuple[int]:
    """
    Calculate page index range
    """
    start = (page - 1) * page_size
    end = start + page_size

    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieve specific page data
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start, end = index_range(page, page_size)

        data = self.dataset()

        return data[start:end]

    def get_hyper(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Union[int, None, List[Any]]]:
        """Paginates a dataset and returns pagination details
        Parameters:
            page (int): The current page number. Defaults to 1.
            page_size (int): The number of items per page. Defaults to 10.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        total_items = len(self.dataset())
        total_pages = (total_items + page_size - 1) // page_size
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        data = self.get_page(page, page_size)

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages":  total_pages
        }
