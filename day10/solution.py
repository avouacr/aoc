import sys

import numpy as np


def parse_grid(file):
    with open(file, 'r') as file_in:
        lines = [line.strip() for line in file_in.readlines()]
        grid_array = np.array([list(line) for line in lines])

    return grid_array


def process_start(grid):
    x_start, y_start = np.where(grid == 'S')
    x_start, y_start = x_start[0], y_start[0]

    directions_to_pipe = {'NS': '|', 'EW': '-', 'NE': 'L', 'NW': 'J', 'SW': '7', 'SE': 'F'}

    adjacent_pipes = []
    directions_adjacent = ''

    # North
    if x_start > 0:
        coords = (x_start - 1, y_start)
        value = grid[x_start - 1, y_start]
        if value in ['|', '7', 'F']:
            adjacent_pipes.append((coords, value))
            directions_adjacent += 'N'

    # East
    if y_start < grid.shape[1] - 1:
        coords = (x_start, y_start + 1)
        value = grid[x_start, y_start + 1]
        if value in ['-', 'J', '7']:
            adjacent_pipes.append((coords, value))
            directions_adjacent += 'E'

    # South
    if x_start < grid.shape[0] - 1:
        coords = (x_start + 1, y_start)
        value = grid[x_start + 1, y_start]
        if value in ['|', 'L', 'J']:
            adjacent_pipes.append((coords, value))
            directions_adjacent += 'S'

    # West
    if y_start > 0:
        coords = (x_start, y_start - 1)
        value = grid[x_start, y_start - 1]
        if value in ['-', 'L', 'F']:
            adjacent_pipes.append((coords, value))
            directions_adjacent += 'W'

    # Replace S with relevant pipe
    if directions_adjacent not in directions_to_pipe:
        directions_adjacent = directions_adjacent[::-1]
    start_pipe = directions_to_pipe[directions_adjacent]
    grid[x_start, y_start] = start_pipe

    # Get one adjacent to start the loop
    adjacent_node = adjacent_pipes[0]

    return grid, ((x_start, y_start), start_pipe), adjacent_node


def get_next_node(grid, node_start, node_inter):
    x_start, y_start = node_start[0]
    x_inter, y_inter = node_inter[0]
    value_inter = node_inter[1]

    if x_inter > x_start:
        # Coming from North
        if value_inter == '|':
            coords_final = (x_inter + 1, y_inter)
        elif value_inter == 'L':
            coords_final = (x_inter, y_inter + 1)
        elif value_inter == 'J':
            coords_final = (x_inter, y_inter - 1)
    elif x_inter < x_start:
        # Coming from South
        if value_inter == '|':
            coords_final = (x_inter - 1, y_inter)
        elif value_inter == '7':
            coords_final = (x_inter, y_inter - 1)
        elif value_inter == 'F':
            coords_final = (x_inter, y_inter + 1)
    elif y_inter > y_start:
        # Coming from West
        if value_inter == '-':
            coords_final = (x_inter, y_inter + 1)
        elif value_inter == 'J':
            coords_final = (x_inter - 1, y_inter)
        elif value_inter == '7':
            coords_final = (x_inter + 1, y_inter)
    elif y_inter < y_start:
        # Coming from East
        if value_inter == '-':
            coords_final = (x_inter, y_inter - 1)
        elif value_inter == 'L':
            coords_final = (x_inter - 1, y_inter)
        elif value_inter == 'F':
            coords_final = (x_inter + 1, y_inter)
    else:
        raise ValueError

    return (coords_final, grid[coords_final])


def build_graph(grid, node_start, node_adjacent):
    n_start, n_inter = node_start, node_adjacent
    next_node = (('x', 'x'), 'x')

    graph = np.zeros(grid.shape)
    graph[node_start[0]] = 1
    graph[node_adjacent[0]] = 1

    steps = 1
    while next_node[0] != node_start[0]:
        next_node = get_next_node(grid, n_start, n_inter)
        graph[next_node[0]] = 1
        n_start = n_inter
        n_inter = next_node
        steps += 1

    sol_part_1 = int(steps / 2)

    return graph, sol_part_1


def main1(file):
    grid = parse_grid(file)
    grid, node_start, node_adjacent = process_start(grid)
    return build_graph(grid, node_start, node_adjacent)[1]


def count_tiles_inside_loop(grid, graph):

    n_inside_loop = 0

    for i in range(grid.shape[0]):
        inside_loop = False
        last_corner = ''
        for j in range(grid.shape[1]):
            if graph[i, j]:
                if grid[i, j] == '|':
                    # Cross border
                    inside_loop = not inside_loop
                elif grid[i, j] in ['L', 'F']:
                    last_corner = grid[i, j]
                elif grid[i, j] in ['J', '7']:
                    if last_corner == 'L' and grid[i, j] == '7':
                        # Cross border
                        inside_loop = not inside_loop
                    elif last_corner == 'F' and grid[i, j] == 'J':
                        # Cross border
                        inside_loop = not inside_loop
            else:
                n_inside_loop += int(inside_loop)

    return n_inside_loop


def main2(file):
    grid = parse_grid(file)
    grid, node_start, node_adjacent = process_start(grid)
    graph, _ = build_graph(grid, node_start, node_adjacent)

    return count_tiles_inside_loop(grid, graph)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1('calibration11.txt') == 4
            assert main1('calibration12.txt') == 8
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2('calibration21.txt') == 4
            assert main2('calibration22.txt') == 8
            assert main2('calibration23.txt') == 10
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
