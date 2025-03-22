from typing import List


# Heuristique somme des aires des espaces vides au carrés
def basic_score(grid: List[List[bool]]) -> float:
    done = []
    areas = []

    def find_area(i, j):
        # Si on dépasse les dimensions de la grille, on est déjà passé par là ou on est sur un gâteau, on renvoie 0
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or (i, j) in done or grid[i][j]:
            return 0
        done.append((i, j))
        return 1 + find_area(i + 1, j) + find_area(i - 1, j) + find_area(i, j + 1) + find_area(i, j - 1)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Si on est déjà passé par là ou si on est sur un gâteau, on passe
            if (i, j) in done or grid[i][j]:
                continue

            areas.append(find_area(i, j))

    return sum(area ** 2 for area in areas)

# Heuristique somme des aires des espaces vides au carrés
def basic2_score(grid: List[List[bool]]) -> float:
    done = []
    total = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Si on est déjà passé par là ou si on est sur un gâteau, on passe
            if (i, j) in done or grid[i][j]:
                continue

            total += 1

    return total


    
# Heuristique somme des aires des espaces vides au carrés
def cake_area_score(x, y, grid) -> float:
    done = []

    def find_area(i, j):
        # Si on dépasse les dimensions de la grille, on est déjà passé par là ou si on est pas sur un gateau
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or (i, j) in done or grid[i][j] != 0:
            return 0
        done.append((i, j))
        return 1 + find_area(i + 1, j) + find_area(i - 1, j) + find_area(i, j + 1) + find_area(i, j - 1)

    return find_area(x, y)


def cake_area_score_2(x, y, grid) -> float:
    done = []
    to_do = [(x, y)]

    while to_do:
        x, y = to_do.pop()
        done.append((x, y))

        for i, j in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x, y) not in done and 0 <= x + i < grid.x and 0 <= x + j < grid.y:
                to_do.append((x + i, y + j))

    return len(done)
