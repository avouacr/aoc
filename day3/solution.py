import sys
import numpy as np


def get_pos_characters(mat):
    disallowed = list(range(10)) + ["."]
    is_char = ~np.isin(mat, disallowed)
    char_pos = np.where(is_char)
    return [(char_pos[0][i], char_pos[1][i]) for i in range(len(char_pos[0]))]


def get_adjacent_coordinates(matrix, x, y):
    # Dimensions of the matrix
    max_x, max_y = matrix.shape

    # List to store adjacent coordinates
    adjacent_coords = []

    # Looping through adjacent positions
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            # Skip the center position
            if dx == 0 and dy == 0:
                continue

            nx, ny = x + dx, y + dy

            # Check if the new position is within the matrix bounds
            if 0 <= nx < max_x and 0 <= ny < max_y:
                adjacent_coords.append((nx, ny))

    return adjacent_coords


def get_full_number(matrix, x, y):

    # Find the start of the number (move left)
    start_y = y
    while start_y > 0 and matrix[x, start_y - 1].isdigit():
        start_y -= 1

    # Find the end of the number (move right)
    end_y = y
    while end_y < matrix.shape[1] - 1 and matrix[x, end_y + 1].isdigit():
        end_y += 1

    # Construct the full number
    number = ''.join(matrix[x, start_y:(end_y + 1)])

    return int(number), (x, start_y)


def main1(file):
    with open(file, 'r') as f:
        matrix = f.read()

    rows = matrix.strip().split('\n')
    matrix = np.array([list(row) for row in rows])
    pos_char = get_pos_characters(matrix)
    candidates = []

    # Find candidate numbers
    for x, y in pos_char:
        adj_coords = get_adjacent_coordinates(matrix, x, y)
        for x_adj, y_adj in adj_coords:
            if matrix[x_adj, y_adj].isdigit():
                candidates.append(get_full_number(matrix, x_adj, y_adj))

    final_numbers = list(set(candidates))
    final_numbers = [x[0] for x in final_numbers]

    return sum(final_numbers)


def get_pos_stars(matrix):
    char_pos = np.where(matrix == '*')
    return [(char_pos[0][i], char_pos[1][i]) for i in range(len(char_pos[0]))]


def main2(file):
    with open(file, 'r') as f:
        matrix = f.read()

    rows = matrix.strip().split('\n')
    matrix = np.array([list(row) for row in rows])

    pos_char = get_pos_stars(matrix)
    gear_ratios = []

    # Find candidate numbers
    for x, y in pos_char:
        candidates = []
        adj_coords = get_adjacent_coordinates(matrix, x, y)
        for x_adj, y_adj in adj_coords:
            if matrix[x_adj, y_adj].isdigit():
                candidates.append(get_full_number(matrix, x_adj, y_adj))

        final_numbers = list(set(candidates))
        if len(final_numbers) == 2:
            final_numbers = [x[0] for x in final_numbers]
            ratio = final_numbers[0] * final_numbers[1]
            gear_ratios.append(ratio)

    return sum(gear_ratios)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 4361
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == 467835
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
