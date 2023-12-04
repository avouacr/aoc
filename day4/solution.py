import sys


def compute_points(card):
    # Splitting the data row into two parts
    parts = card.split(' | ')

    # Parsing the two lists of numbers
    list1 = [int(num) for num in parts[0].split(' ') if num.isdigit()]
    list2 = [int(num) for num in parts[1].split(' ') if num.isdigit()]

    # Counting how many numbers from list2 are in list1
    common = set(list1) & set(list2)
    if len(common) == 1:
        points = 1
    elif len(common) > 1:
        points = 2**(len(common)-1)
    else:
        points = 0

    return points


def main1(file):

    with open(file, 'r') as file:
        lines = file.read().splitlines()

    sum_points = 0
    for card in lines:
        sum_points += compute_points(card)

    return sum_points

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
            assert main1(file="calibration.txt") == 13
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == 30
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
