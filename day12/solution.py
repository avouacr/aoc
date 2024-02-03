import sys
from functools import cache


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
    pattern = row.split(' ')[0]
    rules = tuple(int(n) for n in row.split(' ')[1].split(','))
    return pattern, rules


@cache
def count_valid_patterns(pattern, rules):

    # print(pattern, rules)

    if not rules and '#' not in pattern:
        return 1
    elif not rules and '#' in pattern:
        return 0
    elif not pattern and rules:
        return 0

    if pattern[0] == '.':
        return count_valid_patterns(pattern[1:], rules)
    elif pattern[0] == '#':
        rule = rules[0]
        fits = pattern[:rule].replace('?', '#') == ('#' * rule)
        if len(pattern) > rule:
            next_is_free = pattern[rule] in '.?'
        else:
            next_is_free = True
        if fits and next_is_free:
            return count_valid_patterns(pattern[rule+1:], rules[1:])
        else:
            return 0
    else:
        return count_valid_patterns('.' + pattern[1:], rules) + count_valid_patterns('#' + pattern[1:], rules)


def main(file, expand_rows=False):

    n_combi = 0
    for row in parse_file(file, expand_rows):
        pattern, rules = parse_row(row)
        n_combi += count_valid_patterns(pattern, rules)

    return n_combi


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
            sol_part2 = main(file="puzzle.txt", expand_rows=True)
            print(sol_part2)
