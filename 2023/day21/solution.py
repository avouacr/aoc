import sys

import numpy as np


def parse_grid(file):
    with open(file, 'r') as file_in:
        lines = [line.strip() for line in file_in.readlines()]
        grid = np.array([list(line) for line in lines])

    # Get starting position
    x_start, y_start = np.where(grid == 'S')
    x_start, y_start = x_start[0], y_start[0]

    # Get hash positions
    pos_hash = np.where(grid == '#')
    pos_hash = set([(x, y) for x, y in zip(pos_hash[0], pos_hash[1])])

    return grid, (x_start, y_start), pos_hash


def count_reachable_positions(grid, start, pos_hash, n_steps):
    n_rows, n_cols = grid.shape
    dp = np.zeros((n_rows, n_cols, n_steps + 1), dtype=int)
    dp[start[0], start[1], 0] = 1

    for step in range(1, n_steps + 1):
        for x in range(n_rows):
            for y in range(n_cols):
                if (x, y) not in pos_hash:
                    dp[x, y, step] = (
                        int(dp[x - 1, y, step - 1] > 0 if x > 0 else 0) or
                        int(dp[x + 1, y, step - 1] > 0 if x < n_rows - 1 else 0) or
                        int(dp[x, y - 1, step - 1] > 0 if y > 0 else 0) or
                        int(dp[x, y + 1, step - 1] > 0 if y < n_cols - 1 else 0)
                    )

    n_reachable = np.sum(dp[:, :, n_steps] > 0)
    return n_reachable


def main1(file, n_steps):
    grid, start, pos_hash = parse_grid(file)
    return count_reachable_positions(grid, start, pos_hash, n_steps)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt", n_steps=6) == 16
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt", n_steps=64)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
