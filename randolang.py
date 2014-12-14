from collections import defaultdict
import copy
import random
import os

import nltk

from phones_to_word import phones_to_word


def generate_transitions(phones, order=1):
    """Takes a list of cmudict phones and generates a list of transitions pairs."""
    padded_phones = ['START']*order + phones + ['STOP']*order
    transitions = []
    for index in range(len(padded_phones) - order):
        transition = padded_phones[index:index + order + 1]
        transition = _clean_phones(transition)
        transitions.append(transition)
    return transitions


def _clean_phones(phones):
    """Strips emphasis, etc. from phones."""
    phones_copy = copy.copy(phones)
    return [phone.strip('0123456789') for phone in phones_copy]


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
        if first  not in markov_tree:
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
    while prior_sequence != ['STOP']*order and iters <= max_sequence_size + order - 1:
        iters +=1
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


def entries_from_cmudict(filt=None):
    """Create a list of entries from the cmu corpus.
    If filt='Austen', only uses words that appear in Jane Austen's Emma.
    """
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    if filt is None:
        entries = nltk.corpus.cmudict.entries()
    elif filt == 'Austen':
        entry_dict = nltk.corpus.cmudict.dict()
        entries = nltk.corpus.cmudict.entries()
        filter_words = austen_words()
        filtered_entries = [(entry[0], entry[1]) for entry in entries if entry[0] in filter_words]
        entries = filtered_entries
    return entries


def entries_from_mhyph(filt=None):
    """Create a list of entries from the mhyph corpus.
    If filt='Austen', only uses words that appear in Jane Austen's Emma.
    """
    cwd = os.getcwd()
    mhyph_path = 'data/corpora/gutenberg/mhyph.txt'
    mhyph_full_path = os.path.join(cwd, mhyph_path)
    sequences = []
    with open(mhyph_full_path, 'r') as fin:
        entries = {}
        lines = fin.readlines()
        for line in lines:
            # Only use single words
            if ' ' in line or '-' in line:
                continue
            line = line.strip()
            syllables = line.split('\xa5')
            word = ''.join(syllables)
            entries[word] = syllables
        words = sorted([word for word in entries])
        if filt == 'Austen':
            filter_words = austen_words()
            sequences = [entries[word] for word in words if word in filter_words]
        else:
            sequences = [entries[word] for word in words]
    return sequences


def austen_words():
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    emma_tokenized = nltk.corpus.gutenberg.words('austen-emma.txt')
    emma_words = set([token.lower() for token in emma_tokenized])
    return emma_words
