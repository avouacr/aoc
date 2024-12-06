import sys

import numpy as np
from tqdm import tqdm


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


def get_new_grid(grid):
    new_grid = []
    for j in range(grid.shape[1]):
        col = grid[:, j]
        new_pos_O = get_new_positions_O(col)
        new_col = np.array(['.' if elem == 'O' else elem for i, elem in enumerate(col)])
        new_col[new_pos_O] = 'O'
        new_grid.append(new_col)

    return np.column_stack(new_grid)


def compute_col_load(col, pos_O):
    total_load = sum((len(col) - pos) for pos in pos_O)
    return total_load


def compute_total_load(grid):
    total_load = 0
    for j in range(grid.shape[1]):
        col = grid[:, j]
        pos_O = np.where(col == 'O')[0]
        total_load += compute_col_load(col, pos_O)
    return total_load


def main1(file):
    grid = parse_file(file)

    total_load = 0
    for j in range(grid.shape[1]):
        col = grid[:, j]
        new_pos_O = get_new_positions_O(col)
        total_load += compute_col_load(col, new_pos_O)

    return total_load


def make_cycle(grid):
    grid_n = get_new_grid(grid)
    grid_w = np.rot90(get_new_grid(np.rot90(grid_n, axes=(1, 0))), k=-1, axes=(1, 0))
    grid_s = np.flip(get_new_grid(np.flip(grid_w, 0)), 0)
    grid_e = np.rot90(get_new_grid(np.rot90(grid_s, axes=(1, 0), k=-1)), axes=(1, 0))

    return grid_e


def main2(file):
    grid = parse_file(file)
    store_loop = []
    start_idx = 800  # The sequences has started cycling
    for i, _ in tqdm(enumerate(range(1200))):
        grid = make_cycle(grid)
        if i > start_idx:
            store_loop.append(compute_total_load(grid))

    # Find periodicity
    loop_factor = round(len(store_loop) / store_loop.count(store_loop[0]))

    return store_loop[(int(1e9) - start_idx - 2) % loop_factor]


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
            assert main2(file="calibration.txt") == 64
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
