import sys
from collections import deque

import numpy as np
import networkx as nx


def parse_grid(file, part):
    with open(file, 'r') as file_in:
        lines = [line.strip() for line in file_in.readlines()]
        grid_array = np.array([list(line) for line in lines])

    if part == 2:
        grid_array[np.isin(grid_array, ['<', '>', 'v', '^'])] = '.'

    return grid_array


def is_valid_neighbour1(candidate, visited, grid):
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

    return candidates


def get_longest_path1(grid):

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
        candidates = get_candidates(current, grid, directions, this_node_visited, part=1)
        candidates = [can for can in candidates if is_valid_neighbour1(can, visited, grid)]
        for can in candidates:
            queue.append((can, this_node_visited))

    return max([len(path) for path in valid_paths])


def main1(file):
    grid = parse_grid(file, part=1)
    return get_longest_path1(grid)


def get_corners(grid, directions):
    n_rows, n_cols = grid.shape
    corners = set()
    for x in range(n_rows):
        for y in range(n_cols):
            if grid[x, y] == '.':
                n_valid_neighbors = 0
                if x > 0 and grid[x + directions['U'][0], y + directions['U'][1]] != '#':
                    n_valid_neighbors += 1
                if x < n_rows - 1 and grid[x + directions['D'][0], y + directions['D'][1]] != '#':
                    n_valid_neighbors += 1
                if y > 0 and grid[x + directions['L'][0], y + directions['L'][1]] != '#':
                    n_valid_neighbors += 1
                if y < n_cols - 1 and grid[x + directions['R'][0], y + directions['R'][1]] != '#':
                    n_valid_neighbors += 1
                if n_valid_neighbors >= 3:
                    corners.add((x, y))
    corners.add((n_rows - 1, n_cols - 2))
    return corners


def is_valid_neighbour2(candidate, last_corner, visited, grid):
    x, y = candidate
    not_forest = (grid[x, y] != '#')
    not_visited = (candidate not in visited) and (candidate != last_corner)
    return not_forest and not_visited


def build_compressed_graph(grid, corners, directions, part):
    n_rows, n_cols = grid.shape
    G = nx.Graph()
    visited = set()

    start = (0, 1)
    queue = deque([(start, start)])

    while queue:
        current, last_corner = queue.popleft()
        visited.add(current)
        candidates = get_candidates(current, grid, directions, visited, part)
        candidates = [can for can in candidates
                      if is_valid_neighbour2(can, last_corner, visited, grid)]
        if not candidates:
            continue
        n_steps = 0
        while current not in corners:
            current = candidates[0]
            visited.add(current)
            n_steps += 1
            candidates = get_candidates(current, grid, directions, visited, part)
            candidates = [can for can in candidates
                          if is_valid_neighbour2(can, last_corner, visited, grid)]
        visited.remove(current)
        if candidates:
            G.add_edge(last_corner, current, weight=n_steps+1)
            for can in candidates:
                queue.append((can, current))
        if current == (n_rows - 1, n_cols - 2):
            G.add_edge(last_corner, current, weight=n_steps+1)

    return G


def get_longest_path2(G, grid):
    n_rows, n_cols = grid.shape
    longest_path = 0
    for i, path in enumerate(nx.all_simple_paths(G, (0, 1), (n_rows - 1, n_cols - 2))):
        longest_path = max(longest_path, nx.path_weight(G, path, 'weight') - 1)
        if i > 100000:
            break
    return longest_path


def main2(file):
    grid = parse_grid(file, part=2)
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    corners = get_corners(grid, directions)
    G = build_compressed_graph(grid, corners, directions, part=2)
    return get_longest_path2(G, grid)


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
            assert main2(file="calibration.txt") == 154
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
