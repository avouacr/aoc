import sys
import math
import itertools


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


def compute_steps_part1(instructions, mapping):
    instruction_to_int = {'L': 0, 'R': 1}

    node = 'AAA'
    step = 0
    while node != 'ZZZ':
        direction_int = instruction_to_int[instructions[step % len(instructions)]]
        node = mapping[node][direction_int]
        step += 1
    return step


def get_next_node(node, direction_int, mapping):
    return mapping[node][direction_int]


def compute_steps_part2(instructions, mapping):
    instruction_to_int = {'L': 0, 'R': 1}

    starting_nodes = [n for n in mapping.keys() if n[-1] == 'A']

    steps_to_z = []
    for node in starting_nodes:
        for step, instruction in enumerate(itertools.cycle(instructions)):
            if node.endswith("Z"):
                steps_to_z.append(step)
                break
            direction_int = instruction_to_int[instruction]
            node = get_next_node(node, direction_int, mapping)

    # Needed because each individual path loops
    lcm_steps_to_z = math.lcm(*steps_to_z)

    return lcm_steps_to_z


def main(file, f_compute_steps):
    instructions, mapping = parse_input(file)
    n_steps = f_compute_steps(instructions, mapping)
    return n_steps


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main('calibration11.txt', f_compute_steps=compute_steps_part1) == 2
            assert main('calibration12.txt', f_compute_steps=compute_steps_part1) == 6
        elif MODE == "main":
            sol_part1 = main(file="puzzle.txt", f_compute_steps=compute_steps_part1)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main(file="calibration2.txt", f_compute_steps=compute_steps_part2) == 6
        elif MODE == "main":
            sol_part2 = main(file="puzzle.txt", f_compute_steps=compute_steps_part2)
            print(sol_part2)
