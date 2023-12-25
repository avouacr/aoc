import sys
import re


def parse_condition(condition):
    if '<' in condition:
        letter, value = condition.split('<')
        alt = f'{letter}>={value}'
    else:
        letter, value = condition.split('>')
        alt = f'{letter}<={value}'
    return condition, alt


def parse_input(file):
    with open(file, 'r') as file_in:
        data = file_in.read().split('\n\n')

    workflows = {}
    for wf in data[0].splitlines():
        wf_name, wf_rules = wf.split('{')
        workflows[wf_name] = {}
        alts = []
        for rule in wf_rules.replace('}', '').split(','):
            if ':' in rule:
                condition, destination = rule.split(':')
                condition, alt = parse_condition(condition)
                if alts:
                    condition = ' and '.join(alts + [condition])
                workflows[wf_name][condition] = destination
                alts.append(alt)
            else:
                key = ' and '.join(alts)
                workflows[wf_name][key] = rule
        if len(set(workflows[wf_name].values())) == 1:
            single_letter = list(workflows[wf_name].values())[0]
            workflows[wf_name] = {'True': single_letter}

    ratings = []
    for part in data[1].splitlines():
        row = part.replace('{', '').replace('}', '').split(',')
        ratings.append(tuple(row))

    return workflows, tuple(ratings)


def validate_part(part_ratings, workflows):

    for statement in part_ratings:
        exec(statement)

    decision = 'in'
    while decision not in ['A', 'R']:
        for wf_rule in workflows[decision]:
            if wf_rule in ['A', 'R']:
                decision = wf_rule
                break
            elif eval(wf_rule):
                decision = workflows[decision][wf_rule]
                break

    return decision


def sum_ratings_accepted(all_ratings, workflows):
    total_ratings = 0
    for part_ratings in all_ratings:
        if validate_part(part_ratings, workflows) == 'A':
            total_ratings += sum([int(rat.split('=')[1]) for rat in part_ratings])

    return total_ratings


def main1(file):

    workflows, ratings = parse_input(file)
    return sum_ratings_accepted(ratings, workflows)


def get_admissible_paths(workflows, start, end, path=[], conditions=[]):
    path = path + [start]
    if start == end:
        return [(path, conditions)]
    if start not in workflows:
        return []
    paths = []
    for condition, node in workflows[start].items():
        if node == end or condition == end:
            paths.append((path + [end], conditions + [condition]))
        elif node and node not in path:  # Avoid cycles
            newpaths = get_admissible_paths(workflows, node, end, path, conditions + [condition])
            paths.extend(newpaths)

    return paths


def process_sequence_conditions(path):
    path = path[1]
    sequence_conditions = []
    for condition in path:
        if 'and' in condition:
            sequence_conditions.extend([c for c in condition.split(' and ')])
        elif condition == 'True':
            continue
        else:
            sequence_conditions.append(condition)
    return sequence_conditions


def intersect_ranges(full, condition):
    match = re.search(r'([xmas])([<>]=?)(\d+)', condition)
    sign = match.group(2)
    value = int(match.group(3))

    if sign == '<':
        cond_range = range(1, value)
    elif sign == '<=':
        cond_range = range(1, value + 1)
    elif sign == '>':
        cond_range = range(value + 1, 4001)
    elif sign == '>=':
        cond_range = range(value, 4001)

    inter = set(full).intersection(set(cond_range))
    inter_range = range(min(inter), max(inter) + 1)

    return inter_range


def count_possible_combinations(path):
    ranges = {letter: range(1, 4001) for letter in ['x', 'm', 'a', 's']}
    for condition in path:
        letter = re.search('([xmas])', condition).group(1)
        ranges[letter] = intersect_ranges(ranges[letter], condition)

    n_combi = 1
    for letter in ranges.keys():
        n_combi *= len(ranges[letter])

    return n_combi


def count_all_possible_combinations(paths):
    n_combi_paths = [count_possible_combinations(path) for path in paths]
    return sum(n_combi_paths)


def main2(file):
    workflows, __ = parse_input(file)
    paths = get_admissible_paths(workflows, 'in', 'A')
    paths = [process_sequence_conditions(p) for p in paths]
    return count_all_possible_combinations(paths)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 19114
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == 167409079868000
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
