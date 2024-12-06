import sys
import re


def count_winning_numbers(card):
    parts = card.split(' | ')

    # Parsing the two lists of numbers
    list1 = [int(num) for num in parts[0].split(' ') if num.isdigit()]
    list2 = [int(num) for num in parts[1].split(' ') if num.isdigit()]

    # Counting how many numbers from list2 are in list1
    common = set(list1) & set(list2)
    return len(common)


def compute_points(card):
    # Splitting the data row into two parts
    n_winning_numbers = count_winning_numbers(card)
    if n_winning_numbers > 0:
        points = 2**(n_winning_numbers - 1)
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


def build_cards_mapping(cards_list):
    mapping = {}
    for card in cards_list:
        card_split = card.split(': ')
        card_id = int(card_split[0].split(' ')[1])
        if card_id not in mapping:
            mapping[card_id] = {
                'winning_number': count_winning_numbers(card),
                'counter': 1
            }

    return mapping


def count_final_cards(cards_mapping):
    mapping = cards_mapping.copy()
    total_counter = 0
    for current_id in list(mapping.keys()):
        while mapping[current_id]['counter'] > 0:
            winning_number = mapping[current_id]['winning_number']
            for i in range(1, winning_number + 1):
                next_id = current_id + i
                if next_id in mapping:
                    mapping[next_id]['counter'] += 1

            # Decrement the counter of the current id
            mapping[current_id]['counter'] -= 1
            total_counter += 1

    return total_counter


def main2(file):

    with open(file, 'r') as file:
        cards_deck = file.read()
        cards_deck = re.sub(r"\s\s+", " ", cards_deck)
        cards_deck = cards_deck.splitlines()

    cards_mapping = build_cards_mapping(cards_deck)
    n_final_cards = count_final_cards(cards_mapping)

    return n_final_cards


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
