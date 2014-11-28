from collections import defaultdict
import random
import os

import nltk

conversions = {
    'AA': 'ah',
    'AE': 'a',
    'AH': 'u',
    'AO': 'aw',
    'AW': 'ou',
    'AY': 'ai',
    'B': 'b',
    'CH': 'ch',
    'D': 'd',
    'DH': 'th',
    'EH': 'e',
    'ER': 'ur',
    'EY': 'ay',
    'F': 'f',
    'G': 'g',
    'HH': 'h',
    'IH': 'i',
    'IY': 'ee',
    'JH': 'j',
    'K': 'c',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'NG': 'ng',
    'OW': 'oh',
    'OY': 'oi',
    'P': 'p',
    'R': 'r',
    'S': 's',
    'SH': 'sh',
    'T': 't',
    'TH': 'th',
    'UH': 'uh',
    'UW': 'oo',
    'V': 'v',
    'W': 'w',
    'Y': 'y',
    'Z': 'z',
    'ZH': 'zh'
}


def phones_to_word(phones):
    """Convert a list of phones like 'AA' to a string.
    Note: Assumes emphasis numbers have been stripped.
    """
    translated_phone_list = [conversions[phone] for phone in phones]
    word = ''.join(translated_phone_list)
    return word


def generate_transitions(phones, order=1):
    """Takes a list of cmudict phones and generates a list of transitions pairs."""
    padded_phones = ['START']*order + phones + ['STOP']*order
    transitions = []
    for index in range(len(padded_phones) - order):
        transition = padded_phones[index:index + order + 1]
        transition = [_clean_phone(phone) for phone in transition]
        transitions.append(transition)
    return transitions


def _clean_phone(phone):
    """Strips emphasis, etc. from phones."""
    return phone.strip('0123456789')


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


def entries_from_cmudict():
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    entries = nltk.corpus.cmudict.entries()
    return entries
