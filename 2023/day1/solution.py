import sys


def part1(input_string):
    # Extracting all digits from the input string
    digits = [int(char) for char in input_string if char.isdigit()]

    # Check if we have at least one digit
    if not digits:
        return None

    # Returning the first and last digit as a combined integer
    return int(str(digits[0]) + str(digits[-1]))


def part2(input_string):
    # Dictionary mapping spelled out numbers and digits to their values
    number_options = {
        'one': 1, '1': 1, 
        'two': 2, '2': 2, 
        'three': 3, '3': 3, 
        'four': 4, '4': 4, 
        'five': 5, '5': 5, 
        'six': 6, '6': 6, 
        'seven': 7, '7': 7, 
        'eight': 8, '8': 8, 
        'nine': 9, '9': 9
    }

    # List to store tuples of (digit, position)
    digit_positions = []

    # Search for each number and all of its positions in the string
    for number, value in number_options.items():
        start = 0  # Initial search position
        while True:
            pos = input_string.find(number, start)
            if pos == -1:
                break  # No more occurrences found
            digit_positions.append((value, pos))
            start = pos + 1  # Update the start position for the next search

    # Sorting the list by position
    digit_positions.sort(key=lambda x: x[1])

    # Extracting the first and last digits
    first_digit = digit_positions[0][0]
    last_digit = digit_positions[-1][0]

    # Returning the first and last digit as a combined integer
    return int(str(first_digit) + str(last_digit))


def unit_tests(file, fun):
    with open(file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        test_input, expected_result = line.split(" ")
        predicted_result = fun(test_input)
        assert predicted_result == int(expected_result)


def main(file, fun):

    with open(file, 'r') as file:
        lines = file.readlines()

    lines = [line.split(" ")[0] for line in lines]
    result = sum(fun(line) for line in lines)

    return result


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            unit_tests(file="calibration1.txt", fun=part1)
            assert main(file="calibration1.txt", fun=part1) == 142
        else:
            sol_part1 = main(file="puzzle.txt", fun=part1)
            print(sol_part1)

    if PART == "2":

        if MODE == "test":
            unit_tests(file="calibration1.txt", fun=part2)
            assert main(file="calibration1.txt", fun=part2) == 142
            unit_tests(file="calibration2.txt", fun=part2)
            assert main(file="calibration2.txt", fun=part2) == 281
            assert part2("xtwone3fourone") == 21
        else:
            sol_part2 = main(file="puzzle.txt", fun=part2)
            print(sol_part2)
