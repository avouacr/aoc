import sys


def extract_mappings(file):

    with open(file, 'r') as file_in:
        text = file_in.read()
    text_mappings = text.split('\n\n')[1:]

    mappings = []
    for m in text_mappings:
        m_rows = [row.split(' ') for row in m.split('\n')[1:]]
        m_rows = [[int(item) for item in sublist] for sublist in m_rows]
        for row in m_rows:
            dst_start, src_start, length = row
            mappings.append((src_start, src_start + length, dst_start - src_start))

    return mappings


def get_mapped_value(mappings, src_value):
    for mapping in mappings:
        src_start, src_end, offset = mapping
        if src_start <= src_value < src_end:
            src_value += offset

    return src_value


def yeild_seeds1(file):
    with open(file, 'r') as file_in:
        text = file_in.read()
    text_parsed = text.split('\n\n')

    seeds = text_parsed[0].split(': ')[1].split(' ')
    seeds = [int(item) for item in seeds]

    for seed in seeds:
        yield seed


def yeild_seeds2(file, every=1):
    with open(file, 'r') as file_in:
        text = file_in.read()
    text_parsed = text.split('\n\n')

    seeds = text_parsed[0].split(': ')[1].split(' ')
    seeds = [int(item) for item in seeds]

    for i in range(0, len(seeds) - 1, 2):
        for seed in range(seeds[i], seeds[i] + seeds[i+1], every):
            yield seed


def main1(file):
    mappings = extract_mappings(file)
    min_location_number = float('inf')
    for seed in yeild_seeds1(file):
        mapped_value = get_mapped_value(mappings, seed)
        print(seed, mapped_value)
        min_location_number = min(min_location_number, mapped_value)

    return min_location_number


def main2(file, yield_every=1000):
    mappings_rows = extract_mappings(file)

    seed_to_loc_number = []
    for seed in yeild_seeds2(file, every=yield_every):
        mapped_value = seed
        for rows in mappings_rows:
            mappings = build_mappings(rows)
            mapped_value = get_mapped_value(mappings, mapped_value)
        seed_to_loc_number.append((seed, mapped_value))

    return seed_to_loc_number



if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration.txt") == 35
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main1(file="calibration.txt") == 46
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
