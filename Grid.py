from dataclasses import dataclass
from typing import List

from Parser import Cake


@dataclass
class BakingCake:
    cake: Cake
    ori_x: int
    ori_y: int


class Grid:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

        self.baking: List[BakingCake] = []

        self.grid: List[List[int]] = [[0 for _ in range(x)] for _ in range(y)]

    def add_cake(self, ori_x: int, ori_y: int, cake: Cake):
        # Check grid
        for x, y in cake.squares:
            pass

    # Update the cakes on the grid by the given time 
    def update_cakes(self, time):
        self.grid = [[max(0, self.grid[x][y] - time) for x in range(self.x)] for y in range(self.y)]
        self.baking = [cake for cake in self.baking if self.grid[cake.ori_x][cake.ori_y] > 0]

    def remove_cake(self, cake: BakingCake):
        pass
