import copy
import random

from markov import generate_markov_tree, generate_new_sequence
from phones_to_word import phones_to_word
from word_data import entries_from_cmudict, entries_from_mhyph, filter_entries


def generate_words(number_of_words=100, max_transitions=30,
                   method='syllables', order=1):
    """Create a list of new words."""
    if method == 'tuples':
        word_tuples = generate_word_tuples(number_of_tuples=number_of_words)
        words = [''.join(tup) for tup in word_tuples]
        return words
    elif method == 'phones':
        entries = entries_from_cmudict()
    elif method == 'syllables':
        entries = entries_from_mhyph()
    entries = filter_entries(entries, 'Austen')
    words = [word for word, phones in entries]
    sequences = [syllables for word, syllables in entries]
    markov_tree = generate_markov_tree(sequences, order=order)

    new_words = []
    for i in range(number_of_words):
        new_sequence = generate_new_sequence(markov_tree, max_transitions)
        if method == 'phones':
            word = phones_to_word(new_sequence)
        elif method == 'syllables':
            word = ''.join(new_sequence)
        # Reject words already in the corpus
        if word in words:
            continue
        new_words.append(word)
    return new_words


def generate_word_tuples(number_of_tuples=100, tuple_length=2):
    entries = entries_from_cmudict()
    entries = filter_entries(entries, 'Austen')
    words = [entry[0] for entry in entries]
    word_tuples = []
    for i in range(number_of_tuples):
        words_tuple = []
        for i in range(tuple_length):
            word = random.choice(words)
            words_tuple.append(word)
        words_tuple = tuple(words_tuple)
        word_tuples.append(words_tuple)
    return word_tuples


def _clean_phones(phones):
    """Strips emphasis, etc. from phones."""
    phones_copy = copy.copy(phones)
    return [phone.strip('0123456789') for phone in phones_copy]
