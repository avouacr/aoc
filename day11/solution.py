import sys
import itertools

import numpy as np


def parse_grid(file):
    with open(file, 'r') as file_in:
        lines = [line.strip() for line in file_in.readlines()]
        grid_array = np.array([list(line) for line in lines])

    return grid_array


def get_coords_galaxies(grid):
    xs, ys = np.where(grid == '#')
    coords_galaxies = []
    for x, y in zip(xs, ys):
        coords_galaxies.append((x, y))

    return coords_galaxies


def manhattan_distance(x, y):
    return abs(y[0] - x[0]) + abs(y[1] - x[1])


def get_rows_to_expand(grid):
    rows_to_expand = []
    for i, row in enumerate(grid):
        if len(np.unique(row)) == 1:
            rows_to_expand.append(i)
    return np.array(rows_to_expand)


def get_coords_after_expansion(x, y, rows_to_expand, cols_to_expand, factor):
    dx = np.sum(rows_to_expand < x) * (factor - 1)
    dy = np.sum(cols_to_expand < y) * (factor - 1)

    return x + dx, y + dy


def sum_shortest_path_lengths(coords_galaxies):

    sum_distances = 0
    for n1, n2 in itertools.combinations(coords_galaxies, 2):
        sum_distances += manhattan_distance(n1, n2)

    return sum_distances


def main(file, expansion_factor=2):
    grid = parse_grid(file)

    rows_to_expand = get_rows_to_expand(grid)
    cols_to_expand = get_rows_to_expand(grid.T)

    galaxies = get_coords_galaxies(grid)
    galaxies_after_expansion = [get_coords_after_expansion(x, y, rows_to_expand, cols_to_expand, expansion_factor) 
                                for (x, y) in galaxies]

    return sum_shortest_path_lengths(galaxies_after_expansion)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main('calibration.txt') == 374
        elif MODE == "main":
            sol_part1 = main(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main('calibration.txt', expansion_factor=10) == 1030
            assert main('calibration.txt', expansion_factor=100) == 8410
        elif MODE == "main":
            sol_part2 = main(file="puzzle.txt", expansion_factor=1000000)
            print(sol_part2)
