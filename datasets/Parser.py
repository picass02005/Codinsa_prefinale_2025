# Copyright: Les meilleurs
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Cake:
    baking_time: int
    squares: List[Tuple[int, int]]

@dataclass
class Dataset:
    w: int
    h: int
    cakes: List[Cake]

def parse_dataset(dataset_txt: str) -> Dataset:
    res = Dataset(w=0, h=0, cakes=[])
    lines = dataset_txt.strip().splitlines()
    res.w = int(lines[0])
    res.h = int(lines[1])
    n = int(lines[2])
    assert 2 * n == len(lines) - 3
    for i in range(n):
        cake_id, baking_time, m = map(int, lines[3 + i * 2].split())
        assert cake_id == i
        raw_coords = list(map(int, lines[3 + i * 2 + 1].split()))
        squares = list(zip(raw_coords[::2], raw_coords[1::2]))
        assert m == len(squares)
        res.cakes.append(Cake(baking_time=baking_time, squares=squares))
    return res
