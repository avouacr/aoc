import sys


def parse_input(file):
    with open(file, 'r') as file_in:
        data = file_in.read().split('\n\n')

    workflows = {}
    for wf in data[0].splitlines():
        wf_name, wf_rules = wf.split('{')
        workflows[wf_name] = {}
        for rule in wf_rules.replace('}', '').split(','):
            rule_split = rule.split(':')
            if len(rule_split) == 2:
                key, val = rule_split
                workflows[wf_name][key] = val
            elif len(rule_split) == 1:
                final = rule_split[0]
                if final in ['A', 'R']:
                    workflows[wf_name][final] = None
                else:
                    workflows[wf_name]['True'] = final

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


def main2(file):

    with open(file, 'r') as file_in:
        lines = file_in.read().splitlines()

    return ""


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
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
