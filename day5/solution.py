import sys


def build_mapping(rows):
    mapping = {}

    # Process specified mappings
    for row in rows:
        dst_start, src_start, length = row
        for i in range(length):
            mapping[src_start + i] = dst_start + i

    return mapping


def extract_seeds_mappings(file):

    with open(file, 'r') as file_in:
        text = file_in.read()

    text_parsed = text.split('\n\n')
    seeds = text_parsed[0].split(': ')[1].split(' ')
    seeds = [int(item) for item in seeds]

    maps = []
    for m in text_parsed[1:]:
        m_rows = [row.split(' ') for row in m.split('\n')[1:]]
        m_rows = [[int(item) for item in sublist] for sublist in m_rows]
        maps.append(m_rows)

    return seeds, maps


def main1(file):
    seeds, mappings_rows = extract_seeds_mappings(file)
    mappings = []
    for rows in mappings_rows:
        mappings.append(build_mapping(rows))

    locations = []
    for seed in seeds:
        correspondance = seed
        for mapping in mappings:
            if correspondance in mapping:
                correspondance = mapping[correspondance]
            else:
                continue
        locations.append(correspondance)

    return min(locations)


def main2(file):

    with open(file, 'r') as file:
        lines = file.read().splitlines()

    return ""


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1(file="calibration1.txt") == 35
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration2.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
