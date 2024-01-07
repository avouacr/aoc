import sys
from collections import deque

import numpy as np
import networkx as nx


def parse_grid(file):
    with open(file, 'r') as file_in:
        lines = [line.strip() for line in file_in.readlines()]
        grid_array = np.array([list(line) for line in lines])

    return grid_array


def is_valid_neighbour(candidate, current, grid, directions):
    (x, y), coming_from = candidate
    not_forest = (grid[x, y] != '#')
    not_going_back = any(current[0] + directions[current[1]] != candidate[0])
    return not_forest and not_going_back


def build_graph(grid):
    n_rows, n_cols = grid.shape
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    G = nx.DiGraph()

    start = (np.array((0, 1)), 'U')
    queue = deque([start])
    while queue:
        current = queue.popleft()
        x, y = current[0]

        candidates = []
        if grid[x, y] == '.':
            if x > 0:
                candidates.append((current[0] + directions['U'], 'D'))  # Going up
            if x < n_rows - 1:
                candidates.append((current[0] + directions['D'], 'U'))  # Going down
            if y > 0:
                candidates.append((current[0] + directions['L'], 'R'))  # Going left
            if y < n_cols - 1:
                candidates.append((current[0] + directions['R'], 'L'))  # Going right
        elif grid[x, y] == '^':
            candidates.append((current[0] + directions['U'], 'D'))
        elif grid[x, y] == 'v':
            candidates.append((current[0] + directions['D'], 'U'))
        elif grid[x, y] == '<':
            candidates.append((current[0] + directions['L'], 'R'))
        elif grid[x, y] == '>':
            candidates.append((current[0] + directions['R'], 'L'))

        candidates_valid = [can for can in candidates
                            if is_valid_neighbour(can, current, grid, directions)]
        for candidate in candidates_valid:
            queue.append(candidate)
            G.add_edge(tuple(current[0]), tuple(candidate[0]))

    return G


def get_longest_simple_path(G, start, end):
    simple_paths = list(nx.all_simple_paths(G, start, end))
    return max([(len(path) - 1) for path in simple_paths])


def main1(file):
    grid = parse_grid(file)
    n_rows, n_cols = grid.shape
    G = build_graph(grid)
    len_longest_path = get_longest_simple_path(G, (0, 1), (n_rows-1, n_cols-2))
    return len_longest_path


def main2(file):

    with open(file, 'r') as file_in:
        lines = file_in.read().splitlines()

    return ""


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 94
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
