import sys


def parse_hexa(hexa_input):
    digit_to_dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    direction = digit_to_dir[hexa_input[-1]]
    n_steps = int(hexa_input[1:-1], 16)
    return direction, n_steps


def parse_input(file, part):
    with open(file, 'r') as file_in:
        steps = file_in.read().splitlines()

    steps = [row.split(' ') for row in steps]
    if part == 1:
        steps = [(direction, int(n_steps)) for direction, n_steps, __ in steps]
    elif part == 2:
        steps = [hexa.replace('(', '').replace(')', '') for __, __, hexa in steps]
        steps = [parse_hexa(hexa) for hexa in steps]

    return steps


def get_min_xy(ranges):
    min_x, min_y = float('inf'), float('inf')
    for start, end in ranges:
        min_x = min(min_x, start[0], end[0])
        min_y = min(min_y, start[1], end[1])
    return min_x, min_y


def get_ranges_and_corners(steps):
    dir_to_array = {
        'U': (-1, 0),
        'D': (1, 0),
        'R': (0, 1),
        'L': (0, -1)
    }

    x, y = 0, 0

    ranges = []
    corners = {}
    for i, (direction, n_steps) in enumerate(steps):
        x_start, y_start = x, y
        x += dir_to_array[direction][0] * n_steps
        y += dir_to_array[direction][1] * n_steps
        ranges.append([(x_start, y_start), (x, y)])

        # Handle corners
        # Case 0 : first row if right travel
        if i == 0 and direction == 'R':
            corners[(0, 0)] = {'is_switch': False}
        # Case 1 : horizontal travel
        if direction == 'L':
            corners[(x, y)] = {'is_switch': False}
            if steps[i-1][0] == steps[i+1][0]:
                corners[(x, y)]['is_switch'] = True
        # Case 2 : vertical travel
        if i + 2 < len(steps):
            if direction in ['D', 'U'] and steps[i+1][0] == 'R':
                corners[(x, y)] = {'is_switch': False}
                if steps[i+2][0] == direction:
                    corners[(x, y)]['is_switch'] = True

    # Translate to have only positive coordinates
    x_min, y_min = get_min_xy(ranges)
    ranges = [((r[0][0] - x_min, r[0][1] - y_min), (r[1][0] - x_min, r[1][1] - y_min)) for r in ranges]
    corners = {(k[0] - x_min, k[1] - y_min): v for k, v in corners.items()}

    return ranges, corners


def get_candidate_ranges(ranges, x):

    candidate_ranges = []
    for r in ranges:
        x_start, y_start = r[0]
        x_end, y_end = r[1]

        if x_start == x_end and y_start > y_end:
            y_start, y_end = y_end, y_start

        cond1 = (x_start < x < x_end or x_end < x < x_start)  # Normal cases : simple border
        cond2 = (x == x_start and y_start != y_end)  # Border cases : corners
        if cond1 or cond2:
            candidate_ranges.append(((x_start, y_start), (x_end, y_end)))

        # Sort ranges in order of appearance from left to right
        candidate_ranges = sorted(candidate_ranges, key=lambda x: x[0][1])

    return candidate_ranges


def get_n_rows(ranges):
    flat_list = [coordinate for sublist in ranges for coordinate in sublist]
    x_coords, y_coords = zip(*flat_list)
    return max(x_coords) + 1


def compute_lava_row(x, ranges, corners, verbose=0):
    lava = 0
    candidate_ranges = get_candidate_ranges(ranges, x)
    if verbose:
        print(candidate_ranges)
    inside = False
    for i, r in enumerate(candidate_ranges):
        x_start, y_start = r[0]
        x_end, y_end = r[1]
        if x_start == x_end and y_start > y_end:
            y_start, y_end = y_end, y_start

        # Normal cases : simple border
        if x_start < x < x_end or x_end < x < x_start:
            inside = not inside
            if inside:
                y_start_next_range = candidate_ranges[i+1][0][1]
                lava += y_start_next_range - y_end
            if not inside:
                lava += 1
            if verbose:
                print("normal", (x_start, y_start), (x_end, y_end), f'lava: {lava}')

        # Border cases : corners
        elif (x_start, y_start) in corners:
            if corners[(x_start, y_start)]['is_switch']:
                inside = not inside
            if inside:
                y_start_next_range = candidate_ranges[i+1][0][1]
                lava += y_start_next_range - y_start
            if not inside:
                lava += y_end - y_start + 1
            if verbose:
                print("corner", (x_start, y_start), (x_end, y_end), corners[(x_start, y_start)]['is_switch'], f'lava: {lava}')

    return lava


def compute_total_lava(ranges, corners):
    n_rows = get_n_rows(ranges)
    lava = 0
    for x in range(n_rows):
        lava += compute_lava_row(x, ranges, corners)
    return lava


def main(file, part):
    steps = parse_input(file, part)
    ranges, corners = get_ranges_and_corners(steps)
    return compute_total_lava(ranges, corners)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main(file="calibration.txt", part=1) == 62
        elif MODE == "main":
            sol_part1 = main(file="puzzle.txt", part=1)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main(file="calibration.txt", part=2) == 952408144115
        elif MODE == "main":
            print('start')
            sol_part2 = main(file="puzzle.txt", part=2)
            print(sol_part2)
