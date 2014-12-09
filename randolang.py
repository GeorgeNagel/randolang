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


def generate_transitions_dict(entries, order=1):
    """Takes entries from the cmudict and converts them to a transitions dict."""
    transitions_dict = {}
    for entry in entries:
        word, pron_list = entry
        transitions = generate_transitions(pron_list, order=order)
        for transition in transitions:
            add_transition_to_dict(transitions_dict, transition)
    return transitions_dict


def add_transition_to_dict(transitions_dict, transition):        
    if len(transition) > 2:
        # Add the next transition to the sub-dict
        first_phone = transition[0]
        subsequent_transition = transition[1:]
        if first_phone not in transitions_dict:
            transitions_dict[first_phone] = {}
        sub_dict = transitions_dict[first_phone]
        sub_dict = add_transition_to_dict(sub_dict, subsequent_transition)
        transitions_dict[first_phone] = sub_dict
    else:
        # Add this transition to the dict
        first_phone, second_phone = transition
        if first_phone  not in transitions_dict:
            transitions_dict[first_phone] = {}
        if second_phone not in transitions_dict[first_phone]:
            transitions_dict[first_phone][second_phone] = 0
        transitions_dict[first_phone][second_phone] += 1
    return transitions_dict


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
    print "Phones: %s" % phones
    novel_word = phones_to_word(phones)
    print "Word: %s" % novel_word
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


def austen_words():
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    emma_tokenized = nltk.corpus.gutenberg.words('austen-emma.txt')
    emma_words = set([token.lower() for token in emma_tokenized])
    return emma_words
