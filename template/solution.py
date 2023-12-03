import sys


def part1(input):
    pass


def part2(input):
    pass


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

    return ""


def main2(file):

    with open(file, 'r') as file:
        lines = file.read().splitlines()

    return ""


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            unit_tests(file="calibration1.txt", fun=part1)
            assert main1(file="calibration1.txt") == ""
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            unit_tests(file="calibration2.txt", fun=part2)
            assert main2(file="calibration2.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
