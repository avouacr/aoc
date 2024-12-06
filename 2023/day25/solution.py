import sys

import networkx as nx


def parse_input(file):
    with open(file) as file_in:
        data = file_in.read().splitlines()

    G = nx.Graph()

    for row in data:
        src, edges_dst = row.split(': ')
        for dst in edges_dst.split(' '):
            G.add_edge(src, dst)
            
    return G


def get_sizes_connected_components(G):
    # Find edges with maximum centrality and remove them
    edges_centralities = nx.centrality.edge_betweenness_centrality(G).items()
    edges_to_remove = sorted(edges_centralities, key=lambda x: x[1], reverse=True)[:3]
    for (src, dst), __ in edges_to_remove:
        G.remove_edge(src, dst)
        
    # Compute the sizes of the remaining (hopefully) two connected components
    sizes_cc = [len(cc) for cc in nx.connected_components(G)]
    if len(sizes_cc) == 2:
        return sizes_cc[0] * sizes_cc[1]
    else:
        raise(ValueError)
        

def main1(file):
    G = parse_input(file)
    return get_sizes_connected_components(G)


def main2(file):

    with open(file, 'r') as file_in:
        lines = file_in.read().splitlines()

    return ""


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1('calibration.txt') == 54
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "test":
            assert main2(file="calibration.txt") == ""
        elif MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
