import sys
from itertools import product
from collections import deque

import numpy as np


def parse_input(file):
    with open(file, 'r') as file_in:
        lines = file_in.read().splitlines()

    max_x, max_y, max_z = 0, 0, 0

    cube_coords = {}
    for i, row in enumerate(lines):
        cube_id = i + 1
        cube_coords[cube_id] = []

        row = row.split('~')
        coord_ranges = [(int(c1), int(c2) + 1)
                        for c1, c2 in zip(row[0].split(','), row[1].split(','))]
        coord_ranges = [range(*c) for c in coord_ranges]
        coordinates = list(product(*coord_ranges))
        for x, y, z in coordinates:
            cube_coords[cube_id].append((z, x, y))
            max_x, max_y, max_z = max(x, max_x), max(y, max_y), max(z, max_z)

    max_zxy = (max_z, max_x, max_y)

    return cube_coords, max_zxy


def is_horizontal(cube_id, cube_coords):
    return len(set([z for z, _, _ in cube_coords[cube_id]])) == 1


def is_slot_free(cube_id, z, grid, cube_coords):
    if is_horizontal(cube_id, cube_coords):
        return all([grid[(z, x, y)] == 0 for __, x, y in cube_coords[cube_id]])
    else:
        height = len(cube_coords[cube_id])
        __, x, y = cube_coords[cube_id][0]
        return all(grid[z:(z+height), x, y] == 0)


def falling(cube_coords, max_zxy):
    max_z, max_x, max_y = max_zxy
    grid_shape = (max_z+1, max_x+1, max_y+1)
    grid = np.full(grid_shape, fill_value=0)

    cube_ids_by_asc_min_depth = sorted(cube_coords.keys(),
                                       key=lambda k: min(v[0] for v in cube_coords[k]))
    new_cube_coords = {cube_id: [] for cube_id in cube_coords}
    for cube_id in cube_ids_by_asc_min_depth:
        z = grid.shape[0] - 1
        while is_slot_free(cube_id, z, grid, cube_coords) and z >= 1:
            z -= 1

        # Update coordinates after fall
        if is_horizontal(cube_id, cube_coords):
            for __, x, y in cube_coords[cube_id]:
                grid[z+1, x, y] = cube_id
                new_cube_coords[cube_id].append((z+1, x, y))
        else:
            height = len(cube_coords[cube_id])
            __, x, y = cube_coords[cube_id][0]
            grid[z+1:(z+1+height), x, y] = cube_id
            for z_new in range(z+1, z+1+height):
                new_cube_coords[cube_id].append((z_new, x, y))
        continue

    return new_cube_coords, grid


def get_supports(new_cube_coords, grid):
    supports = {}
    for cube_id in new_cube_coords:
        supports[cube_id] = set()
        for z, x, y in new_cube_coords[cube_id]:
            value = grid[z+1, x, y]
            if value != 0 and value != cube_id:
                supports[cube_id].add(value)

    is_supported_by = {cube: set() for cube in supports}
    for cube_id, cubes_supported in supports.items():
        for cube_sup in cubes_supported:
            is_supported_by[cube_sup].add(cube_id)

    return supports, is_supported_by


def is_disintegratable(cube_id, supports, is_supported_by):
    decision = True
    for cube in supports[cube_id]:
        supported_by = is_supported_by[cube].copy()
        supported_by.discard(cube_id)
        if not supported_by:
            decision = False
    return decision


def n_disintegratable(supports, is_supported_by):
    counter_disintegratable = 0
    for cube_id in supports:
        counter_disintegratable += is_disintegratable(cube_id, supports, is_supported_by)
    return counter_disintegratable


def main1(file):
    cube_coords, max_zxy = parse_input(file)
    new_cube_coords, grid = falling(cube_coords, max_zxy)
    supports, is_supported_by = get_supports(new_cube_coords, grid)
    return n_disintegratable(supports, is_supported_by)


def count_chain_reaction(cube_id, supports, is_supported_by):
    fallen = {cube_id}
    queue = deque(supports[cube_id])
    while queue:
        nxt = queue.popleft()
        if is_supported_by[nxt].issubset(fallen):
            fallen.add(nxt)
            queue.extend(supports[nxt])

    return max(0, len(fallen) - 1)


def main2(file):
    cube_coords, max_zxy = parse_input(file)
    new_cube_coords, grid = falling(cube_coords, max_zxy)
    supports, is_supported_by = get_supports(new_cube_coords, grid)

    sum_chain_reaction = 0
    for cube_id in supports:
        sum_chain_reaction += count_chain_reaction(cube_id, supports, is_supported_by)
    return sum_chain_reaction


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 5
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == 7
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
