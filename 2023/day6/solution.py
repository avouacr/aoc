import sys
import re


def parse_races_info(file, part):

    with open(file, 'r') as file:
        text = file.read()

    # Splitting the text into lines
    lines = text.strip().split('\n')

    if part == 1:
        times = [int(num) for num in re.findall(r'\d+', lines[0])]
        distances = [int(num) for num in re.findall(r'\d+', lines[1])]
        result = list(zip(times, distances))
    elif part == 2:
        numbers = re.findall(r'\d+', text)
        combined_number1 = int(''.join(numbers[:len(numbers)//2]))
        combined_number2 = int(''.join(numbers[len(numbers)//2:]))
        result = (combined_number1, combined_number2)

    return result


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

    races_info = parse_races_info(file, part=1)

    solution = 1
    for race_time, record_distance in races_info:
        solution *= get_number_ways_record_race(race_time, record_distance)

    return solution


def main2(file):

    races_info = parse_races_info(file, part=2)

    race_time, record_distance = races_info
    solution = get_number_ways_record_race(race_time, record_distance)

    return solution


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
            assert main2(file="calibration.txt") == 71503
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
