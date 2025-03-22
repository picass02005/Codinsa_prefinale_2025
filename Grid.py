from typing import List

from Parser import Cake


class Grid:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

        self.grid: List[List[bool]] = [[False for _ in range(x)] for _ in range(y)]

    def add_cake(self, ori_x: int, ori_y: int, cake: Cake):
        pass

    # Update the cakes on the grid by the given time 
    def update_cakes(self, time):
        pass

    def remove_cake(self, ori_x: int, ori_y: int, cake: Cake):
        pass