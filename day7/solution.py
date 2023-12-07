import sys
from collections import Counter
import functools


def extract_games(file):
    with open(file, 'r') as file_in:
        data = file_in.read().splitlines()

    data = [(row.split()[0], int(row.split()[1])) for row in data]

    return data


def hand_to_strength_rank(hand, part):
    counter = Counter(hand)

    if part == 2:
        if 'J' in counter and set(hand) != {'J'}:
            nb_j = counter.pop('J')
            key_max = max(counter, key=counter.get)
            counter[key_max] += nb_j

    character_counts = list(counter.values())
    if 5 in character_counts:
        return 6
    elif 4 in character_counts:
        return 5
    elif 3 in character_counts and 2 in character_counts:
        return 4
    elif 3 in character_counts and character_counts.count(1) == 2:
        return 3
    elif character_counts.count(2) == 2:
        return 2
    elif character_counts.count(2) == 1 and character_counts.count(1) == 3:
        return 1
    elif max(character_counts) == 1:
        return 0
    else:
        raise ValueError


def compare_two_hands_same_figure(cards_order):

    order_local = cards_order

    def compare(game1, game2):
        cards_order = {card: i for i, card in enumerate(order_local)}

        hand1, hand2 = game1[0], game2[0]
        for char1, char2 in zip(hand1, hand2):
            if char1 != char2:
                if cards_order[char1] < cards_order[char2]:
                    return 1
                else:
                    return -1

    return compare


def main(file, part):
    # Import games
    games = extract_games(file)

    # 1st step : ranking by strength
    games_by_strength_rank = [[] for _ in range(7)]
    for hand, bid in games:
        strength_rank = hand_to_strength_rank(hand, part)
        games_by_strength_rank[strength_rank].append((hand, bid))

    # 2nd step : second ordering by first strongest card
    if part == 1:
        cards_order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    elif part == 2:
        cards_order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    comparison_function = compare_two_hands_same_figure(cards_order)
    final_games_order = []
    for list_figure in games_by_strength_rank:
        list_figure_ordered = sorted(list_figure, key=functools.cmp_to_key(comparison_function))
        final_games_order.extend(list_figure_ordered)

    # Compute total winnings
    total_winnings = 0
    for i, (hand, bid) in enumerate(final_games_order):
        total_winnings += bid * (i+1)

    return total_winnings


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main(file="calibration.txt", part=1) == 6440
        elif MODE == "main":
            sol_part1 = main(file="puzzle.txt", part=1)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main(file="calibration.txt", part=2) == 5905
        elif MODE == "main":
            sol_part2 = main(file="puzzle.txt", part=2)
            print(sol_part2)
