"""Generate sequences based on a Markov process."""
import random


def generate_transitions(sequence, order=1):
    """Generates a list of transitions of order <order>."""
    padded_sequence = ['START']*order + sequence + ['STOP']*order
    transitions = []
    for index in range(len(padded_sequence) - order):
        transition = padded_sequence[index:index + order + 1]
        transitions.append(transition)
    return transitions


def generate_markov_tree(sequences, order=1):
    """Creates a markov tree from a sequence of sequences."""
    markov_tree = {}
    for sequence in sequences:
        transitions = generate_transitions(sequence, order=order)
        for transition in transitions:
            add_transition_to_tree(markov_tree, transition)
    return markov_tree


def add_transition_to_tree(markov_tree, transition):
    if len(transition) > 2:
        # Add the next transition to the sub-dict
        first = transition[0]
        subsequent = transition[1:]
        if first not in markov_tree:
            markov_tree[first] = {}
        sub_tree = markov_tree[first]
        sub_tree = add_transition_to_tree(sub_tree, subsequent)
        markov_tree[first] = sub_tree
    else:
        # Add this transition to the dict
        first, second = transition
        if first not in markov_tree:
            markov_tree[first] = {}
        if second not in markov_tree[first]:
            markov_tree[first][second] = 0
        markov_tree[first][second] += 1
    return markov_tree


def order_from_markov_tree(markov_tree, order=0):
    """Calculate the order of a markov tree."""
    for key in markov_tree:
        _order = order + 1
        if isinstance(markov_tree[key], dict):
            order = order_from_markov_tree(markov_tree[key], order=_order)
        break
    return order


def generate_new_sequence(markov_tree, max_sequence_size):
    """Generate a new based on transition probabilities."""
    order = order_from_markov_tree(markov_tree)
    sequence = ['START'] * order
    prior_sequence = sequence
    iters = 0
    while True:
        if prior_sequence == ['STOP']*order:
            break
        if iters > max_sequence_size + order - 1:
            break
        iters += 1
        next_element = _generate_sequence_element(markov_tree, prior_sequence)
        sequence.append(next_element)
        prior_sequence = sequence[-order:]

    # Remove 'START' and 'STOP' markers
    sequence = sequence[order:-order]
    return sequence


def _generate_sequence_element(markov_tree, prior_sequence):
    """Generate the next element in the markov sequence."""
    sub_tree = markov_tree
    for prior_element in prior_sequence:
        sub_tree = sub_tree[prior_element]
    # Now select the next element based on its probability of occurrence
    possible_nexts = []
    for next_element in sub_tree:
        number_of_appearances = sub_tree[next_element]
        nexts = [next_element]*number_of_appearances
        possible_nexts.extend(nexts)
    next_element = random.choice(possible_nexts)
    return next_element
