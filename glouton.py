import argparse
from typing import List, Tuple

from Grid import Grid
from Parser import Cake, Dataset
from Parser import parse_dataset


def best_action(grid: Grid, cakes: List[Cake]):
    best_score = 0
    best_action = None
    grid = grid.__copy__()

    for cake in cakes:
        for x in range(grid.x):
            for y in range(grid.y):
                added = grid.add_cake(x, y, cake)

                if not added:
                    continue

                score = grid.get_minimum_baking_time()
                if score >= best_score:
                    best_score = score
                    best_action = (x, y, cake)
    return best_action

def glouton(dataset: Dataset):
    # Id, StartTime, X, Y
    result: Tuple[int, int, int, int] = []
    grid = Grid(dataset.w, dataset.h, None, None)
    baked_cakes = []
    raw_cakes = dataset.cakes.copy()
    time = 0

    while len(baked_cakes) != len(dataset.cakes):
        action = best_action(grid, raw_cakes)

        if action is None:
            time += grid.get_minimum_baking_time()
            grid.update_cakes(grid.get_minimum_baking_time())
        else:
            x, y, cake = action
            grid.add_cake(x, y, cake)
            baked_cakes.append(cake)
            raw_cakes.remove(cake)
            
            result.append((dataset.cakes.index(cake), time, x, y))

    print('Time:', time)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_path')

    parsed_args = parser.parse_args()
    with open(parsed_args.dataset_path, "r") as file:
        dataset_txt = file.read()
    dataset = parse_dataset(dataset_txt)

    print(glouton(dataset))
