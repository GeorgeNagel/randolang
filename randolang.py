import copy

from markov import generate_markov_tree, generate_new_sequence
from phones_to_word import phones_to_word
from word_data import entries_from_cmudict, entries_from_mhyph


def generate_words(number_of_words=100, max_transitions=30,
                   method='syllables', order=1):
    """Create a list of new words."""
    if method == 'phones':
        entries = entries_from_cmudict(filt='Austen')
    elif method == 'syllables':
        entries = entries_from_mhyph(filt='Austen')
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


def _clean_phones(phones):
    """Strips emphasis, etc. from phones."""
    phones_copy = copy.copy(phones)
    return [phone.strip('0123456789') for phone in phones_copy]
