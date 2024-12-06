import sys


def parse_file(file):
    with open(file, 'r') as file_in:
        steps = file_in.read().split(',')

    return steps


def hash(input_str):
    current_value = 0
    for char in input_str:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def fill_boxes(steps):
    boxes = {i: {} for i in range(256)}

    for step in steps:
        if '-' in step:
            lens_label = step.split('-')[0]
            box_number = hash(lens_label)
            if lens_label in boxes[box_number]:
                del boxes[box_number][lens_label]
        elif '=' in step:
            lens_label, focal_length = step.split('=')
            box_number = hash(lens_label)
            boxes[box_number][lens_label] = int(focal_length)

    boxes = {box: content for box, content in boxes.items() if content}

    return boxes


def compute_focusing_power(boxes):
    focusing_power = 0
    for box_number in boxes:
        box = boxes[box_number]
        for lens_label in box:
            focusing_power += (1 + box_number) * (list(box.keys()).index(lens_label) + 1) * box[lens_label]

    return focusing_power


def main1(file):
    steps = parse_file(file)
    sum_hashes = sum([hash(step) for step in steps])
    return sum_hashes


def main2(file):
    steps = parse_file(file)
    boxes = fill_boxes(steps)
    return compute_focusing_power(boxes)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1('calibration.txt') == 1320
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2('calibration.txt') == 145
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
