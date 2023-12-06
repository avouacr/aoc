import sys
import re


def parse_races_info(file):

    with open(file, 'r') as file:
        text = file.read()

    # Splitting the text into lines
    lines = text.strip().split('\n')

    # Extracting numbers from each line
    times = [int(num) for num in re.findall(r'\d+', lines[0])]
    distances = [int(num) for num in re.findall(r'\d+', lines[1])]

    # Pairing times and distances
    pairs = list(zip(times, distances))

    return pairs


def distance_traveled(race_time, hold_time):
    return (race_time - hold_time) * hold_time


def get_number_ways_record_race(race_time, record_distance):
    counter = 0
    for hold_time in range(race_time):
        distance_run = distance_traveled(race_time, hold_time)
        if distance_run > record_distance:
            counter += 1
    return counter


def main1(file):

    races_info = parse_races_info(file)

    solution = 1
    for race_time, record_distance in races_info:
        solution *= get_number_ways_record_race(race_time, record_distance)

    return solution


def main2(file):

    with open(file, 'r') as file:
        lines = file.read().splitlines()

    return ""


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 288
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
