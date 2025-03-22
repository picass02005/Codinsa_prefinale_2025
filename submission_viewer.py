#!/usr/bin/python3

import argparse
import math
import pygame
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

class InvalidSubmission(ValueError):
    pass

@dataclass
class CakeSubmission:
    id: int
    time: int
    pos: Tuple[int, int]

@dataclass
class Submission:
    cakes: List[CakeSubmission]

    def score(self, dataset: Dataset) -> int:
        seen = [False for cake in dataset.cakes]
        for index, cake in enumerate(self.cakes):
            if cake.id < 0 or cake.id >= len(dataset.cakes):
                raise InvalidSubmission(f"La ligne {index + 1} contient un ID de gâteau invalide")
            if seen[cake.id]:
                raise InvalidSubmission(f"Le gâteau {cake.id} est cuit plusieurs fois")
            if cake.time < 0 or cake.time > 1e10:
                raise InvalidSubmission(f"La ligne {index + 1} contient un temps hors de l'intervalle autorisé [0, 10^10]")
            seen[cake.id] = True
        for index, value in enumerate(seen):
            if not value:
                raise InvalidSubmission(f"Le gâteau {index} n'est jamais cuit")

        score = 0
        last_cake_and_time_free = [[(-1, 0) for j in range(dataset.h)] for i in range(dataset.w)]
        for cake in sorted(self.cakes, key=lambda cake: cake.time):
            cake_end_time = cake.time + dataset.cakes[cake.id].baking_time
            score = max(score, cake_end_time)
            for dx, dy in dataset.cakes[cake.id].squares:
                x = cake.pos[0] + dx
                y = cake.pos[1] + dy
                if not (0 <= x < dataset.w and 0 <= y < dataset.h):
                    raise InvalidSubmission(f"Le gâteau {cake.id} recouvre la position {(x, y)} qui est en dehors du four")
                if last_cake_and_time_free[x][y][1] > cake.time:
                    raise InvalidSubmission(f"Le gâteau {cake.id} recouvre la position {(x, y)} au temps {cake.time} mais cette position "
                                          f"est déjà occupée par le gâteau {last_cake_and_time_free[x][y][0]} jusqu'au temps {last_cake_and_time_free[x][y][1]}")
                last_cake_and_time_free[x][y] = (cake.id, cake_end_time)
        return score

def parse_submission(submission_txt: str) -> Submission:
    res = Submission(cakes=[])
    for index, line in enumerate(submission_txt.strip().splitlines()):
        elems = line.strip().split()
        if len(elems) != 4:
            raise InvalidSubmission(f"La ligne {index + 1} n'a pas exactement 4 valeurs")
        try:
            id, time, x, y = map(int, elems)
        except ValueError:
            raise InvalidSubmission(f"La ligne {index + 1} contient une valeur non entière")
        res.cakes.append(CakeSubmission(id=id, time=time, pos=(x, y)))
    return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_path')
    parser.add_argument('submission_path')
    parser.add_argument('--scale', default='auto')
    parser.add_argument('--speed', default='auto')

    parsed_args = parser.parse_args()
    with open(parsed_args.dataset_path, "r") as file:
        dataset_txt = file.read()
    dataset = parse_dataset(dataset_txt)

    with open(parsed_args.submission_path, "r") as file:
        submission_txt = file.read()
    submission = parse_submission(submission_txt)

    score = submission.score(dataset)

    if parsed_args.scale == 'auto':
        target_w = 1500
        target_h = 800
        viewer_scale = math.floor(min(target_w / dataset.w, target_h / dataset.h))
    else:
        viewer_scale = int(parsed_args.scale)
    
    if parsed_args.speed == 'auto':
        viewer_speed = score / 20.0
    else:
        viewer_speed = float(parsed_args.speed)

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((dataset.w * viewer_scale, dataset.h * viewer_scale + 75))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 42)
    score_text = font.render(f"Score : {score}", True, "black")
    score_text_pos = score_text.get_rect(center=(0.5 * dataset.w * viewer_scale, dataset.h * viewer_scale + 36))

    running = True
    time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        border_width = round(viewer_scale / 12)
        screen.fill("azure2")
        t = int(time * viewer_speed)
        for cake in submission.cakes:
            if cake.time <= t < cake.time + dataset.cakes[cake.id].baking_time:
                color = pygame.Color("burlywood1").lerp("sienna4", (t - cake.time) / dataset.cakes[cake.id].baking_time)
                border_color = color.lerp("black", 0.5)
                shape = dataset.cakes[cake.id].squares
                for diff in shape:
                    pygame.draw.rect(screen, color, pygame.Rect((cake.pos[0] + diff[0]) * viewer_scale, (cake.pos[1] + diff[1]) * viewer_scale, viewer_scale, viewer_scale))
                    if (diff[0] - 1, diff[1]) not in shape:
                        pygame.draw.rect(screen, border_color, pygame.Rect((cake.pos[0] + diff[0]) * viewer_scale, (cake.pos[1] + diff[1]) * viewer_scale, border_width, viewer_scale))
                    if (diff[0] + 1, diff[1]) not in shape:
                        pygame.draw.rect(screen, border_color, pygame.Rect((cake.pos[0] + diff[0] + 1) * viewer_scale - border_width, (cake.pos[1] + diff[1]) * viewer_scale, border_width, viewer_scale))
                    if (diff[0], diff[1] - 1) not in shape:
                        pygame.draw.rect(screen, border_color, pygame.Rect((cake.pos[0] + diff[0]) * viewer_scale, (cake.pos[1] + diff[1]) * viewer_scale, viewer_scale, border_width))
                    if (diff[0], diff[1] + 1) not in shape:
                        pygame.draw.rect(screen, border_color, pygame.Rect((cake.pos[0] + diff[0]) * viewer_scale, (cake.pos[1] + diff[1] + 1) * viewer_scale - border_width, viewer_scale, border_width))
        pygame.draw.rect(screen, "azure3", pygame.Rect(0, dataset.h * viewer_scale, dataset.w * viewer_scale, 75))
        screen.blit(score_text, score_text_pos)
        pygame.display.flip()
        time += clock.tick(60) / 1000
    pygame.quit()
