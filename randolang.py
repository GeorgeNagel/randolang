import copy
import random

from markov import generate_markov_tree, generate_new_sequence
from phones_to_word import phones_to_word
from tools.words_cache import WordsCache
from word_data import entries_from_cmudict, entries_from_mhyph, filter_entries


def generate_words(number_of_words=100, max_transitions=30,
                   method='syllables', order=1, words_cache=None):
    """Create a list of new words."""
    if words_cache is None:
        words_cache = WordsCache()
    if method == 'tuples':
        words_cache = _generate_words_tuples(
            number_of_words=number_of_words, words_cache=words_cache,
            tuple_length=order
        )
        return words_cache
    elif method == 'phones':
        words_cache = _generate_words_phones(
            number_of_words=number_of_words, words_cache=words_cache,
            order=order, max_transitions=max_transitions
        )
        return words_cache
    elif method == 'syllables':
        words_cache = _generate_words_syllables(
            number_of_words=number_of_words, words_cache=words_cache,
            order=order, max_transitions=max_transitions
        )
        return words_cache


def _generate_words_syllables(number_of_words=100,
                              order=1,
                              max_transitions=30,
                              words_cache=None):
    if words_cache is None:
        words_cache = WordsCache()
    entries = entries_from_mhyph()
    entries = filter_entries(entries, 'Austen')
    existing_words = [word for word, syllables in entries]
    sequences = [syllables for word, syllables in entries]
    markov_tree = generate_markov_tree(sequences, order=order)

    number_generated = 0
    while number_generated < number_of_words:
        cached_words = words_cache.get_words('syllables')
        new_sequence = generate_new_sequence(markov_tree, max_transitions)
        new_word = ''.join(new_sequence)
        # Reject words already in the corpus
        if new_word in existing_words or new_word in cached_words:
            continue
        else:
            words_cache.add_word('syllables', new_word)
            print "New word: %s" % new_word
            number_generated += 1
    return words_cache


def _generate_words_phones(number_of_words=100,
                           order=1,
                           max_transitions=30,
                           words_cache=None):
    if words_cache is None:
        words_cache = WordsCache()
    entries = entries_from_cmudict()
    entries = filter_entries(entries, 'Austen')
    existing_words = [word for word, phones in entries]
    sequences = [phones for word, phones in entries]
    markov_tree = generate_markov_tree(sequences, order=order)

    number_generated = 0
    while number_generated < number_of_words:
        cached_words = words_cache.get_words('phones')
        new_sequence = generate_new_sequence(markov_tree, max_transitions)
        new_word = phones_to_word(new_sequence)
        # Reject words already in the corpus
        if new_word in existing_words or new_word in cached_words:
            continue
        else:
            words_cache.add_word('phones', new_word)
            print "New word: %s" % new_word
            number_generated += 1
    return words_cache


def _generate_words_tuples(number_of_words=100,
                           tuple_length=2,
                           words_cache=None):
    if words_cache is None:
        words_cache = WordsCache()
    entries = entries_from_cmudict()
    entries = filter_entries(entries, 'Austen')
    entry_words = [entry[0] for entry in entries]

    number_generated = 0
    while number_generated < number_of_words:
        cached_words = words_cache.get_words('tuples')
        words_tuple = []
        for i in range(tuple_length):
            word = random.choice(entry_words)
            words_tuple.append(word)
        new_word = ''.join(words_tuple)
        # Don't overwrite data for words already in the cache
        if new_word not in cached_words:
            words_cache.add_word('tuples', new_word)
            print "New word: %s" % new_word
            number_generated += 1
    return words_cache


def _clean_phones(phones):
    """Strips emphasis, etc. from phones."""
    phones_copy = copy.copy(phones)
    return [phone.strip('0123456789') for phone in phones_copy]
