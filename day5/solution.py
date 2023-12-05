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


def generate_seeds(file, part):
    with open(file, 'r') as file_in:
        text = file_in.read()
    text_parsed = text.split('\n\n')

    seeds = text_parsed[0].split(': ')[1].split(' ')
    seeds = [int(item) for item in seeds]

    if part == 1:
        for seed in seeds:
            yield seed
    if part == 2:
        for i in range(0, len(seeds) - 1, 2):
            seeds_expanded = list(range(seeds[i], seeds[i] + seeds[i+1]))
            for seed in seeds_expanded:
                yield seed


def main(file, part, mode='min'):
    mappings_rows = extract_mappings(file)
    locations = []
    for seed in generate_seeds(file, part=part):
        mapped_value = seed
        for rows in mappings_rows:
            mappings = build_mappings(rows)
            mapped_value = get_mapped_value(mappings, mapped_value)
        locations.append(mapped_value)

    if mode == 'all':
        result = locations
    elif mode == 'min':
        result = min(locations)

    return result


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main(file="calibration.txt", part=1, mode='all') == [82, 43, 86, 35]
            assert main(file="calibration.txt", part=1) == 35
        elif MODE == "main":
            sol_part1 = main(file="puzzle.txt", part=1)
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main(file="calibration.txt", part=2) == 46
        elif MODE == "main":
            sol_part2 = main(file="puzzle.txt")
            print(sol_part2)
