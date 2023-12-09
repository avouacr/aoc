import sys


def parse_input(file):
    with open(file, 'r') as file_in:
        data_raw = file_in.read().splitlines()

    data = []
    for row in data_raw:
        row_data = [int(n) for n in row.split(' ')]
        data.append(tuple(row_data))

    return data


def pairwise_differences(sequence):
    # Calculating the differences between every two consecutive integers
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def predict_next_number(sequence):
    last_int_sequences = [sequence[-1]]
    while set(pairwise_differences(sequence)) != {0}:
        sequence = pairwise_differences(sequence)
        last_int_sequences.append(sequence[-1])

    last_int_sequences = last_int_sequences[::-1]
    return sum(last_int_sequences)


def predict_previous_number(sequence):
    first_int_sequences = [sequence[0]]

    while set(pairwise_differences(sequence)) != {0}:
        sequence = pairwise_differences(sequence)
        first_int_sequences.append(sequence[0])

    first_int_sequences = first_int_sequences[::-1]

    result = 0
    for i in range(len(first_int_sequences)):
        result = first_int_sequences[i] - result

    return result


def main(file, f_prediction):
    sequences = parse_input(file)
    predictions = [f_prediction(seq) for seq in sequences]
    return sum(predictions)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main(file="calibration.txt", f_prediction=predict_next_number) == 114
        elif MODE == "main":
            sol_part1 = main(file="puzzle.txt", f_prediction=predict_next_number)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main(file="calibration.txt", f_prediction=predict_previous_number) == 2
        elif MODE == "main":
            sol_part2 = main(file="puzzle.txt", f_prediction=predict_previous_number)
            print(sol_part2)
