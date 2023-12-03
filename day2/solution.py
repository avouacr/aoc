import sys


def part1(input_str):
    game_id = input_str.split(':')[0].split(' ')[1]
    # Splitting the string into segments
    segments = input_str.split(': ')[1].split('; ')

    # Dictionaries to store the max values before each color
    max_values = {'blue': 0, 'red': 0, 'green': 0}

    for segment in segments:
        # Splitting each segment into parts
        parts = segment.split(',')

        for part in parts:
            # Splitting each part into numbers and colors
            words = part.strip().split()
            number, color = int(words[0]), words[1]
            max_values[color] = max(max_values[color], number)

    if max_values["red"] > 12 or max_values["green"] > 13 or max_values["blue"] > 14:
        result = "impossible"
    else:
        result = "possible"

    return int(game_id), result


def part2(input_str):
    game_id = input_str.split(':')[0].split(' ')[1]
    # Splitting the string into segments
    segments = input_str.split(': ')[1].split('; ')

    # Dictionaries to store the max values before each color
    max_values = {'blue': 0, 'red': 0, 'green': 0}

    for segment in segments:
        # Splitting each segment into parts
        parts = segment.split(',')

        for part in parts:
            # Splitting each part into numbers and colors
            words = part.strip().split()
            number, color = int(words[0]), words[1]
            max_values[color] = max(max_values[color], number)

    power = max_values["blue"] * max_values["red"] * max_values["green"]

    return game_id, str(power)


def unit_tests(file, fun):
    with open(file, 'r') as file:
        lines = file.read().splitlines()

    for line in lines:
        test_input, expected_result = line.split(" || ")
        predicted_result = fun(test_input)[1]
        assert predicted_result == expected_result


def main1(file):

    with open(file, 'r') as file:
        lines = file.read().splitlines()

    ids_possible = [int(part1(line)[0]) for line in lines if part1(line)[1] == "possible"]
    result = sum(ids_possible)

    return result


def main2(file):

    with open(file, 'r') as file:
        lines = file.read().splitlines()

    powers = [int(part2(line)[1]) for line in lines ]
    result = sum(powers)

    return result


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            unit_tests(file="calibration1.txt", fun=part1)
            assert main1(file="calibration1.txt", fun=part1) == 8
        else:
            sol_part1 = main1(file="puzzle.txt", fun=part1)
            print(sol_part1)

    if PART == "2":

        if MODE == "test":
            unit_tests(file="calibration2.txt", fun=part2)
            assert main2(file="calibration2.txt") == 2286
        else:
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
