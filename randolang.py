# coding=utf-8
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


def order_from_transitions_dict(transitions_dict, order=0):
    """Calculate the order of a transitions_dict."""
    for key in transitions_dict:
        _order = order + 1
        if isinstance(transitions_dict[key], dict):
            order = order_from_transitions_dict(transitions_dict[key], order=_order)
        break
    return order


def generate_word(transitions_dict, max_phone_size):
    """generate words based on the phoneme transition probabilities."""
    order = order_from_transitions_dict(transitions_dict)
    phones = ['START'] * order
    prior_phones = phones
    iters = 0
    while prior_phones != ['STOP']*order and iters <= max_phone_size + order - 1:
        iters +=1
        next_phone = _generate_phone(transitions_dict, prior_phones)
        phones.append(next_phone)
        prior_phones = phones[-order:]

    # Remove 'START' and 'STOP' markers
    phones = phones[order:-order]
    novel_word = phones_to_word(phones)
    return novel_word

def _generate_phone(transitions_dict, prior_phones):
    """Generate the next phone in the sequence."""
    sub_dict = transitions_dict
    for prior_phone in prior_phones:
        sub_dict = sub_dict[prior_phone]
    # Now select the next phone based on its probability of occurrence
    possible_nexts = []
    for next_phoneme in sub_dict:
        number_of_appearances = sub_dict[next_phoneme]
        nexts = [next_phoneme]*number_of_appearances
        possible_nexts.extend(nexts)
    next_phoneme = random.choice(possible_nexts)
    return next_phoneme


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
    entries = []
    with open(mhyph_full_path, 'r') as fin:
        lines = fin.readlines()
        entries = {}
        for line in lines:
            # Only use single words
            if ' ' in line:
                continue
            syllables = line.split('¥')
            word = ''.join(syllables)
            entries[word] = syllables
        if filt == 'Austen':
            filter_words = austen_words()
            entries = [entry for entry in entries if entry in filter_words]
    return entries


def austen_words():
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    emma_tokenized = nltk.corpus.gutenberg.words('austen-emma.txt')
    emma_words = set([token.lower() for token in emma_tokenized])
    return emma_words
