import sys
import itertools


def parse_input(file):

    with open(file) as file_in:
        data = file_in.read().splitlines()

    data_parsed = []
    for row in data:
        position, velocity = row.split(' @ ')
        position = [int(pos) for pos in position.split(', ')]
        velocity = [int(vel) for vel in velocity.split(', ')]
        data_parsed.append((tuple(position), tuple(velocity)))

    return data_parsed


def compute_equation_line(hailstone):
    p1, (dx, dy, dz) = hailstone
    p2 = (p1[0] + dx, p1[1] + dy, p1[1] + dz)
    slope = (p2[1] - p1[1]) / (p2[0] - p1[0]) if p2[0] - p1[0] != 0 else float('inf')
    intercept = p1[1] - slope * p1[0]
    return slope, intercept


def find_intersection(line1, line2):
    m1, c1 = line1
    m2, c2 = line2

    # Check if lines are parallel
    if m1 == m2:
        return None

    # Calculate intersection point
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    return (x, y)


def is_forward(point, hailstone):
    x, y = point
    hail, velocity = hailstone
    x_is_forward = x > hail[0] if velocity[0] > 0 else x < hail[0]
    y_is_forward = y > hail[1] if velocity[1] > 0 else y < hail[1]
    return x_is_forward and y_is_forward


def is_inside_test_area(intersection, min_test, max_test):
    x_inside = min_test <= intersection[0] <= max_test
    y_inside = min_test <= intersection[1] <= max_test
    return x_inside and y_inside


def count_valid_crossings(hailstones, test_area):
    min_test_area, max_test_area = test_area

    n_valid_crossings = 0
    for hail1, hail2 in itertools.combinations(hailstones, 2):
        line1, line2 = compute_equation_line(hail1), compute_equation_line(hail2)
        intersection = find_intersection(line1, line2)
        if intersection is not None:
            is_forward_crossing = (is_forward(intersection, hail1)
                                   and is_forward(intersection, hail2))
            is_inside_test = is_inside_test_area(intersection, min_test_area, max_test_area)
            if is_forward_crossing and is_inside_test:
                n_valid_crossings += 1

    return n_valid_crossings


def main1(file, test_area):
    hailstones = parse_input(file)
    return count_valid_crossings(hailstones, test_area)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1('calibration.txt', test_area=(7, 27)) == 2
        elif MODE == "main":
            sol_part1 = main1('puzzle.txt', test_area=(200000000000000, 400000000000000))
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
