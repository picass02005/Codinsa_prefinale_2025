from dataclasses import dataclass
from typing import List, Optional

from Parser import Cake


@dataclass
class BakingCake:
    cake: Cake
    ori_x: int
    ori_y: int


class Grid:
    def __init__(self, x: int, y: int, baking: Optional[List[BakingCake]], grid: Optional[List[List[int]]]):
        self.x: int = x
        self.y: int = y

        self.baking: List[BakingCake] = baking if baking is not None else []

        self.grid: List[List[int]] = grid if grid is not None else [[0 for _ in range(x)] for _ in range(y)]

    def copy_grid(self):
        return [y.copy() for y in self.grid]

    def __copy__(self):
        grid = self.__new__(self.__class__)
        grid.__init__(self.x, self.y, self.baking.copy(), self.copy_grid())
        return grid


    def add_cake(self, ori_x: int, ori_y: int, cake: Cake) -> bool:
        new_grid = self.copy_grid()
        for x, y in cake.squares:
            if ori_x + x >= self.x or ori_y + y >= self.y:
                return False

            new_grid[ori_y + y][ori_x + x] = cake.baking_time

            if self.grid[ori_y + y][ori_x + x] != 0:
                # print("WARNING: Tu empile des gateaux sale fou", sys.stderr)
                return False

        self.grid = new_grid
        self.baking.append(BakingCake(cake, ori_x, ori_y))

        return True

    def get_minimum_baking_time(self):
        if len(self.baking) == 0:
            return 0

        return min([self.grid[cake.ori_y][cake.ori_x] for cake in self.baking])

    # Update the cakes on the grid by the given time 
    def update_cakes(self, time):
        self.grid = [[max(0, self.grid[y][x] - time) for x in range(self.x)] for y in range(self.y)]
        self.baking = [cake for cake in self.baking if self.grid[cake.ori_x][cake.ori_y] > 0]
