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


def build_dig(steps):

    dir_to_array = {
        'U': (-1, 0),
        'D': (1, 0),
        'R': (0, 1),
        'L': (0, -1)
    }

    dig = set()
    x, y = 0, 0

    for direction, n_steps in steps:
        for n in range(n_steps):
            x += dir_to_array[direction][0]
            y += dir_to_array[direction][1]
            dig.add((x, y))

    # Start on (0, 0)
    min_x = min(coords[0] for coords in dig)
    min_y = min(coords[1] for coords in dig)
    dig = set([(x - min_x, y - min_y) for x, y in dig])

    return dig


def if_corner_get_direction(x, y, dig):
    direction = ''
    if (x-1, y) in dig:
        direction = 'U'
    elif (x+1, y) in dig:
        direction = 'D'

    if ((x, y-1) in dig or (x, y+1) in dig) and direction:
        return True, direction
    return False, ''


def count_lava(dig):

    n_rows = max(coords[0] for coords in dig) + 1
    n_cols = max(coords[1] for coords in dig) + 1

    lava = 0
    fill = set()
    for x in range(n_rows):
        inside = False
        n_successive_dig = 0
        n_corners_seen = 0
        last_corner_direction = ''
        for y in range(n_cols):
            if (x, y) in dig:
                lava += 1
                n_successive_dig += 1

                is_corner, corner_direction = if_corner_get_direction(x, y, dig)
                if is_corner:
                    # Case of corners
                    if n_corners_seen == 0:
                        # First corner, do nothing
                        last_corner_direction = corner_direction
                        n_corners_seen += 1
                    elif n_corners_seen == 1:
                        # Second corner : if different direction than last one, switch `inside`
                        if last_corner_direction != corner_direction:
                            inside = not inside
                        n_corners_seen = 0
                else:
                    # Normal border : get in or get out
                    if n_successive_dig == 1:
                        inside = not inside

            else:
                if inside:
                    fill.add((x, y))
                    lava += 1
                n_successive_dig = 0

    return lava


def main(file, part):
    steps = parse_input(file, part)
    dig = build_dig(steps)
    return count_lava(dig)


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
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
