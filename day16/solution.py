import sys

import numpy as np


def parse_input(file):

    with open(file, 'r') as file_in:
        rows = file_in.read().splitlines()

    grid = np.array([list(row) for row in rows])
    return grid


def get_row(grid, x_start, y_start, direction):

    n_rows, n_cols = grid.shape

    if direction == 'E':
        row = grid[x_start, (y_start+1):]
    elif direction == 'W':
        row = grid[x_start, ::-1][(n_cols - y_start):]
    elif direction == 'S':
        row = grid[:, y_start][(x_start+1):]
    elif direction == 'N':
        row = grid[:, y_start][::-1][(n_rows - x_start):]

    return row


def process_row(row, x_start, y_start, direction, where_to_mirrors):
    to_process = []
    energized = []

    if row.size > 0:
        i = 0
        while i < len(row):

            if direction == 'E':
                pos_i = (x_start, y_start + i + 1)
            elif direction == 'W':
                pos_i = (x_start, y_start - i - 1)
            elif direction == 'S':
                pos_i = ( x_start + i + 1, y_start)
            elif direction == 'N':
                pos_i = (x_start - i - 1, y_start)

            energized.append(pos_i)

            if row.size == 1 and row[0] == '.':
                break

            if row[i] == '|' and direction in ['E', 'W']:
                to_process.extend([(pos_i, 'N'), (pos_i, 'S')])
                break
            elif row[i] == '-' and direction in ['S', 'N']:
                to_process.extend([(pos_i, 'E'), (pos_i, 'W')])
                break
            elif row[i] in ['/', '\\']:
                where_to = where_to_mirrors[row[i]][direction]
                to_process.extend([(pos_i, where_to)])
                break
            i += 1

    return to_process, energized


def propagate(grid, start_task):
    tasks_done = set()
    queue = [start_task]
    store_energized = set()

    where_to_mirrors = {
        '/': {'E': 'N', 'W': 'S', 'S': 'W', 'N': 'E'},
        '\\': {'E': 'S', 'W': 'N', 'S': 'E', 'N': 'W'}
    }

    while queue:
        (x_start, y_start), direction = queue[0]
        row = get_row(grid, x_start, y_start, direction)
        new_tasks, energized = process_row(row, x_start, y_start, direction, where_to_mirrors)
        store_energized.update(energized)
        queue.extend([task for task in new_tasks if task not in tasks_done])
        tasks_done.add(queue.pop(0))

    return store_energized


def get_possible_starts(grid):
    n_rows, n_cols = grid.shape

    north_face = [((-1, i), 'S') for i in range(n_cols)]
    south_face = [((n_rows, i), 'N') for i in range(n_cols)]
    west_face = [((i, -1), 'E') for i in range(n_rows)]
    east_face = [((i, n_cols), 'W') for i in range(n_rows)]
    possible_starts = north_face + south_face + west_face + east_face

    return possible_starts


def main1(file):
    grid = parse_input(file)
    tiles_energized = propagate(grid, start_task=((0, -1), 'E'))
    return len(tiles_energized)


def main2(file):
    grid = parse_input(file)

    max_energy = 0
    for start in get_possible_starts(grid):
        n_energized = len(propagate(grid, start))
        max_energy = max(max_energy, n_energized)

    return max_energy


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 46
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == 51
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
