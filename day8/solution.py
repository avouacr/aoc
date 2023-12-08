import sys


def parse_input(file):
    with open(file, 'r') as file_in:
        text = file_in.read()

    txt_split = text.split('\n\n')
    instructions = txt_split[0]
    rows = txt_split[1].split('\n')

    mapping = {}
    for row in rows:
        start_node, destinations = row.split(' = ')
        destinations = tuple(destinations.replace('(', '').replace(')', '').split(', '))
        mapping[start_node] = destinations

    return instructions, mapping


def compute_steps(instructions, mapping, start_node='AAA'):
    instruction_to_int = {'L': 0, 'R': 1}

    node = start_node
    step = 0
    while node != 'ZZZ':
        direction = instruction_to_int[instructions[step % len(instructions)]]
        node = mapping[node][direction]
        step += 1
    return step


def main1(file):
    instructions, mapping = parse_input(file)
    n_steps = compute_steps(instructions, mapping)
    return n_steps


def main2(file):

    with open(file, 'r') as file_in:
        lines = file_in.read().splitlines()

    return ""


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1('calibration11.txt') == 2
            assert main1('calibration12.txt') == 6
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
