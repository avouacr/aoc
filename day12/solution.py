import sys
import itertools


def expand(row):
    pattern, rules = row.split(' ')
    pattern = '?'.join([pattern] * 5)
    rules = ','.join([rules] * 5)
    return pattern + ' ' + rules


def parse_file(file, expand_rows):
    with open(file, 'r') as file_in:
        rows = [line.strip() for line in file_in.readlines()]

    if expand_rows:
        rows = [expand(row) for row in rows]

    return rows


def parse_row(row):
    pattern = list(row.split(' ')[0])
    rules = tuple(int(n) for n in row.split(' ')[1].split(','))
    return pattern, rules


def get_candidates(pattern, rules):
    n_springs_to_add = sum(rules) - pattern.count('#')
    coords_qm = [i for i, char in enumerate(pattern) if char == '?']

    candidates = []
    for combination in itertools.combinations(coords_qm, n_springs_to_add):
        cand = pattern.copy()
        for coord in combination:
            cand[coord] = '#'
        candidates.append(cand)

    return candidates


def is_valid(pattern, rules):
    lengths_blocs_springs = tuple([sum(1 for _ in g) for k, g in itertools.groupby(pattern)
                                   if k == '#'])
    return 1 if lengths_blocs_springs == rules else 0


def main(file, expand_rows=False):

    count_valid = 0
    for row in parse_file(file, expand_rows):
        pattern, rules = parse_row(row)
        candidates = get_candidates(pattern, rules)
        for cand in candidates:
            count_valid += is_valid(cand, rules)

    return count_valid


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main('calibration.txt') == 21
        elif MODE == "main":
            sol_part1 = main('puzzle.txt')
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main('calibration.txt', expand_rows=True) == 525152
        elif MODE == "main":
            sol_part2 = main(file="puzzle.txt")
            print(sol_part2)
