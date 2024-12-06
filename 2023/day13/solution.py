import sys


def parse_file(file):
    with open(file, 'r') as file_in:
        text = file_in.read()

    patterns = text.split('\n\n')
    patterns = [(p.splitlines()) for p in patterns]

    return patterns


def pattern_to_list(pattern, transpose=False):
    return [list(row) for row in pattern]


def transpose_pattern(pattern_l):
    return [list(i) for i in zip(*pattern_l)]


def flatten(list_input):
    return [x for xs in list_input for x in xs]


def can_be_identical_by_one_change(list1, list2):
    list1, list2 = flatten(list1), flatten(list2)
    differences = sum(1 for a, b in zip(list1, list2) if a != b)
    return differences == 1


def is_symmetry(pattern_l, idx, part):

    assert idx > 0 and idx < len(pattern_l)

    left = pattern_l[:idx]
    right = pattern_l[idx:]

    if len(left) > len(right):
        left = left[(len(left) - len(right)):]
    else:
        right = right[:len(left)]

    if part == 1:
        test_symmetry = (left == right[::-1])
    elif part == 2:
        # If smudge
        test_symmetry = can_be_identical_by_one_change(left, right[::-1])

    return test_symmetry


def search_symmetry(pattern_l, part):
    for idx_sym in range(1, len(pattern_l)):
        if is_symmetry(pattern_l, idx_sym, part):
            return idx_sym

    return 0


def count_solution_pattern(pattern, part):
    pattern_l = pattern_to_list(pattern)

    idx_sym_h = search_symmetry(pattern_l, part)  # Horizontal search
    if idx_sym_h:
        return len(pattern_l[:idx_sym_h]) * 100

    pattern_l_T = transpose_pattern(pattern_l)
    idx_sym_v = search_symmetry(pattern_l_T, part)  # Vertical search
    if idx_sym_v:
        return len(pattern_l_T[:idx_sym_v])


def main(file, part):
    patterns = parse_file(file)
    result = 0
    for pattern in patterns:
        sol_pattern = count_solution_pattern(pattern, part)
        result += sol_pattern
    return result


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main('calibration.txt', part=1) == 405
        elif MODE == "main":
            sol_part1 = main('puzzle.txt', part=1)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main('calibration.txt', part=2) == 400
        elif MODE == "main":
            sol_part2 = main('puzzle.txt', part=2)
            print(sol_part2)
