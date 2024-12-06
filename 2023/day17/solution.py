import sys
from heapq import heappush, heappop

import numpy as np


def parse_input(file):
    with open(file, 'r') as file_in:
        rows = file_in.read().splitlines()
    rows = [[int(x) for x in r] for r in rows]
    return np.array(rows)


def get_neighbours_part1(grid, n):
    x, y, from_dir, n_last_turn = n
    n_rows, n_cols = grid.shape
    neighbours = []

    if n == (0, 0, None, None):
        neighbours.extend([(0, 1, 'W', 1), (1, 0, 'N', 1)])

    # When coming from North, can't move North
    if from_dir == 'N':
        if y > 0:  # Move West
            neighbours.append((x, y - 1, 'E', 1))
        if y < n_cols - 1:  # Move East
            neighbours.append((x, y + 1, 'W', 1))
        if (x < n_rows - 1) and (n_last_turn < 3):  # Move South
            neighbours.append((x + 1, y, 'N', n_last_turn+1))

    # When coming from West, can't move West
    elif from_dir == 'W':
        if x > 0:  # Move North
            neighbours.append((x - 1, y, 'S', 1))
        if x < n_rows - 1:  # Move South
            neighbours.append((x + 1, y, 'N', 1))
        if (y < n_cols - 1) and (n_last_turn < 3):  # Move East
            neighbours.append((x, y + 1, 'W', n_last_turn+1))

    # When coming from South, can't move South
    elif from_dir == 'S':
        if y > 0:  # Move West
            neighbours.append((x, y - 1, 'E', 1))
        if y < n_cols - 1:  # Move East
            neighbours.append((x, y + 1, 'W', 1))
        if x > 0 and (n_last_turn < 3):  # Move North
            neighbours.append((x - 1, y, 'S', n_last_turn+1))

    # When coming from East, can't move East
    elif from_dir == 'E':
        if x > 0:  # Move North
            neighbours.append((x - 1, y, 'S', 1))
        if x < n_rows - 1:  # Move South
            neighbours.append((x + 1, y, 'N', 1))
        if y > 0 and (n_last_turn < 3):  # Move West
            neighbours.append((x, y - 1, 'E', n_last_turn+1))

    return neighbours


def get_neighbours_part2(grid, n):
    x, y, from_dir, n_last_turn = n
    n_rows, n_cols = grid.shape
    neighbours = []

    if n == (0, 0, None, None):
        neighbours.extend([(0, 1, 'W', 1), (1, 0, 'N', 1)])

    # When coming from North, can't move North
    if from_dir == 'N':
        if n_last_turn < 4:
            if x < n_rows - 1:
                neighbours.append((x + 1, y, 'N', n_last_turn+1))
        else:
            if y > 0:  # Move West
                neighbours.append((x, y - 1, 'E', 1))
            if y < n_cols - 1:  # Move East
                neighbours.append((x, y + 1, 'W', 1))
            if x < n_rows - 1 and n_last_turn < 10:  # Move South
                neighbours.append((x + 1, y, 'N', n_last_turn+1))

    # When coming from West, can't move West
    elif from_dir == 'W':
        if n_last_turn < 4:
            if y < n_cols - 1:
                neighbours.append((x, y + 1, 'W', n_last_turn+1))
        else:
            if x > 0:  # Move North
                neighbours.append((x - 1, y, 'S', 1))
            if x < n_rows - 1:  # Move South
                neighbours.append((x + 1, y, 'N', 1))
            if y < n_cols - 1 and n_last_turn < 10:  # Move East
                neighbours.append((x, y + 1, 'W', n_last_turn+1))

    # When coming from South, can't move South
    elif from_dir == 'S':
        if n_last_turn < 4:
            if x > 0:
                neighbours.append((x - 1, y, 'S', n_last_turn+1))
        else:
            if y > 0:  # Move West
                neighbours.append((x, y - 1, 'E', 1))
            if y < n_cols - 1:  # Move East
                neighbours.append((x, y + 1, 'W', 1))
            if x > 0 and n_last_turn < 10:  # Move North
                neighbours.append((x - 1, y, 'S', n_last_turn+1))

    # When coming from East, can't move East
    elif from_dir == 'E':
        if n_last_turn < 4:
            if y > 0:
                neighbours.append((x, y - 1, 'E', n_last_turn+1))
        else:
            if x > 0:  # Move North
                neighbours.append((x - 1, y, 'S', 1))
            if x < n_rows - 1:  # Move South
                neighbours.append((x + 1, y, 'N', 1))
            if y > 0 and n_last_turn < 10:  # Move West
                neighbours.append((x, y - 1, 'E', n_last_turn+1))

    return neighbours


def dijkstra(grid, f_get_neighbours):
    priority_queue = []
    s_deb = (0, 0, None, None)
    heappush(priority_queue, (0, s_deb))

    cost_so_far = {}
    cost_so_far[s_deb] = 0

    came_from = {}
    came_from[s_deb] = None

    while priority_queue:
        current_node = heappop(priority_queue)[1]
        for next_node in f_get_neighbours(grid, current_node):
            new_cost = cost_so_far[current_node] + grid[next_node[0], next_node[1]]
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                heappush(priority_queue, (new_cost, next_node))
                came_from[next_node] = current_node

    min_heat_loss = min([v for k, v in cost_so_far.items()
                         if (k[0] == grid.shape[0] - 1) and k[1] == grid.shape[1] - 1])

    return min_heat_loss


def main1(file):
    grid = parse_input(file)
    min_heat_loss = dijkstra(grid, get_neighbours_part1)
    return min_heat_loss


def main2(file):
    grid = parse_input(file)
    min_heat_loss = dijkstra(grid, get_neighbours_part2)
    return min_heat_loss


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1('calibration.txt') == 102
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2('calibration.txt') == 94
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
