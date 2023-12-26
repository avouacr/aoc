import sys
import re
from collections import deque


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
            network[module] = Test(name=module)

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


class Test:
    def __init__(self, name):
        self.name = name
        self.nature = 'test'
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
            print([(module_name_previous, input_signal, module.name) for module_name_previous, input_signal, module in queue])
            print()

    return counts


def repeat_push_button(n, network):
    total_counts = {'low': 0, 'high': 0}
    for i in range(n):
        counts = push_button(network)
        total_counts['low'] += counts['low']
        total_counts['high'] += counts['high']
    return total_counts['low'] * total_counts['high']


def push_button_until(network):
    count = 0
    while network['rx'].input_signal != 'low':
        push_button(network)
        count += 1
    return count


def main1(file):
    network = parse_input(file)
    return repeat_push_button(n=1000, network=network)


def main2(file):
    network = parse_input(file)
    return push_button_until(network)


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
