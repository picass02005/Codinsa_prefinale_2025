import os
import sys
from typing import List, Tuple

import submission_viewer
from Grid import Grid
from Parser import Cake, Dataset
from Parser import parse_dataset
from scores import *


def best_action(grid: Grid, cakes: List[Cake]):
    best_score = 0
    best_action = None
    grid = grid.__copy__()

    for cake in cakes:
        size = len(cake.squares)
        available_space = grid.x * grid.y - sum(sum(x != 0 for x in y) for y in grid.grid)

        if size > available_space:
            # print('Not enough space for cake', cake.identifier)
            continue

        for x in range(grid.x):
            for y in range(grid.y):
                added = grid.add_cake(x, y, cake)

                if not added:
                    continue

                if cake.identifier == 16:
                    print(cake.identifier, x, y, added)

                # score = basic2_score(grid.grid)
                score = cake_area_score(x, y, grid.grid)
                if score >= best_score:
                    best_score = score
                    best_action = (x, y, cake)
    return best_action

def glouton(dataset: Dataset):
    # Id, StartTime, X, Y
    result: Tuple[int, int, int, int] = []
    grid = Grid(dataset.w, dataset.h, None, None)
    baked_cakes = []
    raw_cakes = sorted(dataset.cakes, key=lambda cake: len(cake.squares), reverse=True)
    time = 0

    while len(baked_cakes) != len(dataset.cakes):
        action = best_action(grid, raw_cakes)

        print(len(baked_cakes), "/", len(dataset.cakes))

        if action is None:
            time += grid.get_minimum_baking_time()
            grid.update_cakes(grid.get_minimum_baking_time())
        else:
            x, y, cake = action

            grid.add_cake(x, y, cake)
            baked_cakes.append(cake)
            raw_cakes.remove(cake)

            result.append((cake.identifier, time, x, y))

    print('Time:', time)
    return result

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dataset_path = f'datasets/{os.listdir("datasets")[int(input("Gwive dwatwaswet nwumber\n>>> ")) - 1]}'

    else:
        dataset_path = sys.argv[1]

    print(f"{dataset_path = }")
    with open(dataset_path, "r") as file:
        dataset_txt = file.read()
    dataset = parse_dataset(dataset_txt)

    with open("aout_put.txt", "w") as f:
        for i in glouton(dataset):
            f.write(f"{' '.join(str(j) for j in i)}\n")

    submission_viewer.run(dataset_path, "aout_put.txt", 50, 100)
