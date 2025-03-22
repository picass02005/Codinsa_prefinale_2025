from typing import List

from Parser import Cake


class Grid:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

        self.grid: List[List[bool]] = [[False for _ in range(x)] for _ in range(y)]

    def add_cake(self, cake: Cake):
        pass

    def remove_cake(self, cake: Cake):
        pass