
from collections import deque

from tqdm import tqdm


def parse_input(file):
    with open(file) as file_in:
        patterns, designs = file_in.read().split('\n\n')

    patterns = set(patterns.split(', '))
    designs = designs.splitlines()

    return patterns, designs


def get_patterns_beginning(patterns, design):
    return [pat for pat in patterns if pat == design[:len(pat)]]


def is_possible(design, patterns):
    possible_patterns = [pat for pat in patterns if pat in design]
    queue = deque(get_patterns_beginning(possible_patterns, design))
    seen = set()

    while queue:
        pat = queue.popleft()
        len_pat = len(pat)
        seen.add(pat)

        if pat == design:
            return True
        
        candidates = get_patterns_beginning(possible_patterns, design[len_pat:])
        if candidates:
            queue.extend([pat + cand for cand in candidates if pat + cand not in seen])

    return False


def main1(file):
    patterns, designs = parse_input(file)

    n_designs_possible = 0
    for design in tqdm(designs):
        n_designs_possible += is_possible(design, patterns)

    return n_designs_possible


def count_valid_ways(design, patterns):
    possible_patterns = [pat for pat in patterns if pat in design]
    queue = deque(get_patterns_beginning(possible_patterns, design))
    seen_parts = set()
    valid_ways = set()

    while queue:
        pat_parts = queue.popleft()
        pat_full = pat_parts.replace(',', '')
        len_pat = len(pat_full)
        seen_parts.add(pat_parts)

        if pat_full == design:
            valid_ways.add(pat_parts)

        candidates = get_patterns_beginning(possible_patterns, design[len_pat:])
        if candidates:
            queue.extend([f'{pat_parts},{cand}' for cand in candidates 
                        if f'{pat_parts},{cand}' not in seen_parts])

    return len(valid_ways)


def main2(file):
    patterns, designs = parse_input(file)

    n_valid_ways = 0
    for design in tqdm(designs):
        n_valid_ways += count_valid_ways(design, patterns)

    return n_valid_ways


assert main1('example1.txt') == 6


main1('input.txt')


assert main2('example1.txt') == 16


main2('input.txt')





