from typing import List, Dict

books: List[Dict] = []


class Book:
    def __init__(self, id: int, title: str, author: str, year: int):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
