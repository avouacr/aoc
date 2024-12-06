import sys
import re
from collections import deque
import copy
import math

import networkx as nx


def parse_input(file):

    with open(file) as file_in:
        data = file_in.read().splitlines()

    network = {}

    # Build network
    dst_modules_history = set()
    for relation in data:
        dst_modules = tuple(relation.split('-> ')[1].split(', '))
        if len(dst_modules) == 1:
            dst_modules = tuple([dst_modules[0]])
        for module in dst_modules:
            dst_modules_history.add(dst_modules[0])

        if 'broadcaster' in relation:
            network['broadcaster'] = Broadcaster(name='broadcaster', dst_modules=dst_modules)
        elif re.search(r'%(\w+)', relation):
            flip_flop = re.search(r'%(\w+)', relation).group(1)
            network[flip_flop] = FlipFlop(name=flip_flop, dst_modules=dst_modules)
        elif re.search(r'&(\w+)', relation):
            conjunction = re.search(r'&(\w+)', relation).group(1)
            network[conjunction] = Conjunction(name=conjunction, dst_modules=dst_modules)

    # Add input modules for conjunction type modules
    for module in network:
        for dst in network[module].dst_modules:
            if dst in network and network[dst].nature == 'conjunction':
                network[dst].input_signals[module] = 'low'

    # Add test modules to the network
    for module in dst_modules_history:
        if module not in network:
            network[module] = Unsigned(name=module)

    return network


class Broadcaster:
    def __init__(self, name, dst_modules):
        self.name = name
        self.nature = 'broadcaster'
        self.dst_modules = dst_modules

    def send_pulse(self, input_signal, module_name_previous, network):
        next_modules = [(self.name, input_signal, network[module]) for module in self.dst_modules]
        return next_modules


class FlipFlop:
    def __init__(self, name, dst_modules):
        self.name = name
        self.nature = 'flip_flop'
        self.dst_modules = dst_modules
        self.is_on = False

    def send_pulse(self, input_signal, module_name_previous, network):
        # If input signal is low, witch state and output signal
        if input_signal == 'low':
            self.is_on = not self.is_on
            if self.is_on:
                signal_out = 'high'
            else:
                signal_out = 'low'

        # If input signal is high, do nothing
        else:
            return []

        next_modules = [(self.name, signal_out, network[module]) for module in self.dst_modules]
        return next_modules


class Conjunction:
    def __init__(self, name, dst_modules):
        self.name = name
        self.nature = 'conjunction'
        self.dst_modules = dst_modules
        self.input_signals = {}

    def send_pulse(self, input_signal, module_name_previous, network):
        # Change state of input
        self.input_signals[module_name_previous] = input_signal
        # Decide output signal based on input states
        input_signals = self.input_signals.values()
        signal_out = 'low' if (set(input_signals) == {'high'}) else 'high'

        next_modules = [(self.name, signal_out, network[module]) for module in self.dst_modules]
        return next_modules


class Unsigned:
    def __init__(self, name):
        self.name = name
        self.nature = 'unsigned'
        self.input_signal = ''

    def send_pulse(self, input_signal, module_name_previous, network):
        self.input_signal = input_signal
        return []


def push_button(network, verbose=0):
    counts = {'low': 0, 'high': 0}
    # Push button
    queue = deque([('button', 'low', network['broadcaster'])])
    while queue:
        module_name_previous, input_signal, module = queue.popleft()
        counts[input_signal] += 1
        dst_modules_input_signals = module.send_pulse(input_signal=input_signal,
                                                      module_name_previous=module_name_previous,
                                                      network=network)
        queue.extend(dst_modules_input_signals)
        if verbose:
            print(module_name_previous, input_signal, module.name)
            print([(module_name_previous, input_signal, module.name)
                   for module_name_previous, input_signal, module in queue])
            print()

    return counts


def repeat_push_button(n, network):
    total_counts = {'low': 0, 'high': 0}
    for i in range(n):
        counts = push_button(network)
        total_counts['low'] += counts['low']
        total_counts['high'] += counts['high']
    return total_counts['low'] * total_counts['high']


def main1(file):
    network = parse_input(file)
    return repeat_push_button(n=1000, network=network)


def build_subgraphs(network):

    # Build full networkx graph
    G = nx.DiGraph()
    for src in network:
        if hasattr(network[src], 'dst_modules'):
            for dst in network[src].dst_modules:
                G.add_edge(src, dst)

    # Compute subgraphs
    last_conjunction_inputs = list(network['gh'].input_signals.keys())
    subgraphs = []
    for lci in last_conjunction_inputs:
        asp = nx.all_simple_paths(G, 'broadcaster', lci)
        subgraph_nodes = set(n for path in asp for n in path)
        subgraph_nodes.add('gh')
        subgraph = {name: module for name, module in network.items() if name in subgraph_nodes}
        subgraph = copy.deepcopy(subgraph)
        for module in subgraph.values():
            if hasattr(module, 'dst_modules'):
                module.dst_modules = tuple([dst for dst in module.dst_modules
                                            if dst in subgraph_nodes])
            if hasattr(module, 'input_signals'):
                module.input_signals = {k: v for k, v in module.input_signals.items()
                                        if k in subgraph_nodes}

        subgraphs.append(subgraph)

    return subgraphs


def get_loop_size(subgraph, n_press_button, verbose=0):
    indxs = []
    for n in range(n_press_button):
        queue = deque([('button', 'low', subgraph['broadcaster'])])
        while queue:
            module_name_previous, input_signal, module = queue.popleft()
            if module.name == 'gh' and input_signal == 'high':
                indxs.append(n)
            dst_modules_input_signals = module.send_pulse(input_signal=input_signal,
                                                          module_name_previous=module_name_previous,
                                                          network=subgraph)
            queue.extend(dst_modules_input_signals)

    loop_size = indxs[1] - indxs[0]
    return loop_size


def main2(file):
    # Explanation : gh sends a low signal to rx when its 4 inputs are high
    # So for each of the 4 subgraphs, we check when the last node sends a high to gh
    # Checked : this happens every nth button push, with n being constant from the start
    # So we get the n by comparing any two subsequent occurences
    # gh sends a low signal when the four subgraphs synchronize on a high
    # This is the lcm for each cycle cycle size (since it starts at 0)
    network = parse_input(file)
    subgraphs = build_subgraphs(network)

    subgraph_loop_sizes = []
    for subgraph in subgraphs:
        subgraph_loop_sizes.append(get_loop_size(subgraph, n_press_button=10000, verbose=0))

    return math.lcm(*subgraph_loop_sizes)


if __name__ == "__main__":

    PART = sys.argv[1]
    MODE = sys.argv[2]

    if PART == "1":

        if MODE == "test":
            assert main1('calibration11.txt') == 32000000
            assert main1('calibration12.txt') == 11687500
        elif MODE == "main":
            sol_part1 = main1(file="puzzle.txt")
            print(sol_part1)

    elif PART == "2":

        if MODE == "main":
            sol_part2 = main2(file="puzzle.txt")
            print(sol_part2)
