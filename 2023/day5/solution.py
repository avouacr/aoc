import sys


def extract_mappings(file):

    with open(file, 'r') as file_in:
        text = file_in.read()
    text_mappings = text.split('\n\n')[1:]

    maps = []
    for m in text_mappings:
        m_rows = [row.split(' ') for row in m.split('\n')[1:]]
        m_rows = [[int(item) for item in sublist] for sublist in m_rows]
        maps.append(m_rows)

    return maps


def build_mappings(rows):
    mappings = []

    for row in rows:
        dst_start, src_start, length = row
        mappings.append((src_start, src_start + length, dst_start - src_start))

    return mappings


def get_mapped_value(mappings, src_value):
    for mapping in mappings:
        src_start, src_end, offset = mapping
        if src_start <= src_value < src_end:
            return src_value + offset
    return src_value


def get_seeds(file):
    with open(file, 'r') as file_in:
        text = file_in.read()
    text_parsed = text.split('\n\n')

    seeds = text_parsed[0].split(': ')[1].split(' ')
    seeds = [int(item) for item in seeds]

    return seeds


def main1(file):
    mappings_rows = extract_mappings(file)
    min_location_number = float('inf')
    for seed in get_seeds(file):
        mapped_value = seed
        for rows in mappings_rows:
            mappings = build_mappings(rows)
            mapped_value = get_mapped_value(mappings, mapped_value)
        min_location_number = min(min_location_number, mapped_value)

    return min_location_number


def extract_seed_ranges(file):
    with open(file, 'r') as file_in:
        text = file_in.read()
    text_parsed = text.split('\n\n')

    seeds = text_parsed[0].split(': ')[1].split(' ')
    seeds = [int(item) for item in seeds]

    seed_ranges = []
    for i in range(0, len(seeds) - 1, 2):
        seed_ranges.append((seeds[i], seeds[i] + seeds[i+1]))

    return seed_ranges


def get_best_range(seed_ranges, mappings_rows, yield_every):
    min_location_number_per_seed_range = []
    for seed_start, seed_stop in seed_ranges:
        min_location_number = float('inf')
        for seed in range(seed_start, seed_stop, yield_every):
            mapped_value = seed
            for rows in mappings_rows:
                mappings = build_mappings(rows)
                mapped_value = get_mapped_value(mappings, mapped_value)
            min_location_number = min(min_location_number, mapped_value)
        min_location_number_per_seed_range.append(min_location_number)

    best_range_idx = min_location_number_per_seed_range.index(min(min_location_number_per_seed_range))
    best_range = seed_ranges[best_range_idx]

    return best_range


def split_range(start, end, n_splits):
    range_size = (end - start) // n_splits
    ranges = [(start + i * range_size, min(start + (i + 1) * range_size - 1, end)) for i in range(10)]
    return ranges


def main2(file):

    mappings_rows = extract_mappings(file)

    # Get best range candidate from sampling procedure
    seed_ranges = extract_seed_ranges(file)
    best_range = get_best_range(seed_ranges, mappings_rows, yield_every=1000)

    # Recursively splitting and finding best range candidate with decay of approximation
    n_order_approx = 2
    for i in range(n_order_approx):
        print(f'Order of approximation {i}')
        range_start, range_stop = best_range
        n_splits = 10 // (i+1)
        ranges_sub = split_range(range_start, range_stop, n_splits=n_splits)
        yield_every = 1000 // 10**i
        best_range = get_best_range(ranges_sub, mappings_rows, yield_every)

    # Brute search to find the minimum location number in the
    # final best range candidate
    seed_start, seed_stop = best_range
    print(f'Brute search : {seed_stop - seed_start} seeds to try')
    min_location_number = float('inf')
    for seed in range(seed_start, seed_stop):
        mapped_value = seed
        for rows in mappings_rows:
            mappings = build_mappings(rows)
            mapped_value = get_mapped_value(mappings, mapped_value)
        min_location_number = min(min_location_number, mapped_value)

    return min_location_number


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

        if MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
