import sys

import numpy as np


def parse_file(file):
    with open(file, 'r') as file_in:
        rows = [list(row) for row in file_in.read().splitlines()]

    return np.array(rows)


def get_first_positions(arr):
    n_O = len(np.where(arr == 'O')[0])
    return [pos for pos in range(n_O)]


def get_new_positions_O(col):
    hashes = np.where(col == '#')[0]
    sub_arrays = [np.array(list(sub)) for sub in ''.join(col).split('#')]

    new_pos_O = []
    for i, arr in enumerate(sub_arrays):
        pos_O_in_sub = get_first_positions(arr)
        if i == 0:
            new_pos_O.extend(pos_O_in_sub)
        else:
            new_pos_O.extend([hashes[i-1] + j + 1 for j in pos_O_in_sub])

    return new_pos_O


def compute_load(col):
    new_pos_O = get_new_positions_O(col)
    col_load = sum((len(col) - pos) for pos in new_pos_O)
    return col_load


def main1(file):
    grid = parse_file(file)
    total_load = 0
    for j in range(grid.shape[1]):
        total_load += compute_load(grid[:, j])
    return total_load


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 136
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
