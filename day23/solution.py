import sys
from collections import deque

import numpy as np


def parse_grid(file, part):
    with open(file, 'r') as file_in:
        lines = [line.strip() for line in file_in.readlines()]
        grid_array = np.array([list(line) for line in lines])

    if part == 2:
        grid_array[np.isin(grid_array, ['<', '>', 'v', '^'])] = '.'

    return grid_array


def is_valid_neighbour(candidate, visited, grid):
    x, y = candidate
    not_forest = (grid[x, y] != '#')
    not_visited = candidate not in visited
    return not_forest and not_visited


def get_candidates(current, grid, directions, visited, part):
    n_rows, n_cols = grid.shape
    x, y = current
    candidates = []
    if part == 1:
        if grid[x, y] == '.':
            if x > 0 and grid[x + directions['U'][0], y + directions['U'][1]] != 'v':
                candidates.append((x + directions['U'][0], y + directions['U'][1]))  # Going up
            if x < n_rows - 1 and grid[x + directions['U'][0], y + directions['U'][1]] != '^':
                candidates.append((x + directions['D'][0], y + directions['D'][1]))  # Going down
            if y > 0 and grid[x + directions['U'][0], y + directions['U'][1]] != '>':
                candidates.append((x + directions['L'][0], y + directions['L'][1]))  # Going left
            if y < n_cols - 1 and grid[x + directions['U'][0], y + directions['U'][1]] != '<':
                candidates.append((x + directions['R'][0], y + directions['R'][1]))  # Going right
        elif grid[x, y] == '^':
            candidates.append((x + directions['U'][0], y + directions['U'][1]))
        elif grid[x, y] == 'v':
            candidates.append((x + directions['D'][0], y + directions['D'][1]))
        elif grid[x, y] == '<':
            candidates.append((x + directions['L'][0], y + directions['L'][1]))
        elif grid[x, y] == '>':
            candidates.append((x + directions['R'][0], y + directions['R'][1]))

    elif part == 2:
        if grid[x, y] == '.':
            if x > 0:
                candidates.append((x + directions['U'][0], y + directions['U'][1]))  # Going up
            if x < n_rows - 1:
                candidates.append((x + directions['D'][0], y + directions['D'][1]))  # Going down
            if y > 0:
                candidates.append((x + directions['L'][0], y + directions['L'][1]))  # Going left
            if y < n_cols - 1:
                candidates.append((x + directions['R'][0], y + directions['R'][1]))  # Going right

    candidates = [cand for cand in candidates if is_valid_neighbour(cand, visited, grid)]
    return candidates


def get_longest_path(grid, part):

    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    n_rows, n_cols = grid.shape

    valid_paths = []
    start = ((0, 1), set())
    queue = deque([start])
    while queue:
        current, visited = queue.popleft()
        if current == (n_rows - 1, n_cols - 2):
            valid_paths.append(visited)
        this_node_visited = visited.copy()
        this_node_visited.add(current)
        candidates = get_candidates(current, grid, directions, this_node_visited, part)
        for can in candidates:
            queue.append((can, this_node_visited))

    return max([len(path) for path in valid_paths])


def main(file, part):
    grid = parse_grid(file, part)
    return get_longest_path(grid, part)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main(file="calibration.txt", part=1) == 94
        elif MODE == "main":
            sol_part1 = main(file="puzzle.txt", part=1)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main(file="calibration.txt", part=2) == 154
        elif MODE == "main":
            sol_part2 = main(file="puzzle.txt", part=2)
            print(sol_part2)
