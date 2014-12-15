import copy
import os

import nltk

from markov import generate_markov_tree, generate_new_sequence
from phones_to_word import phones_to_word


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


def entries_from_cmudict(filt=None):
    """Create a list of entries from the cmu corpus.
    If filt='Austen', only uses words that appear in Jane Austen's Emma.
    """
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    entries = nltk.corpus.cmudict.entries()
    if filt == 'Austen':
        filter_words = austen_words()
        entries = [(entry[0], entry[1]) for entry in entries
                   if entry[0] in filter_words]
    return entries


def entries_from_mhyph(filt=None):
    """Create a list of entries from the mhyph corpus.
    If filt='Austen', only uses words that appear in Jane Austen's Emma.
    """
    cwd = os.getcwd()
    mhyph_path = 'data/corpora/gutenberg/mhyph.txt'
    mhyph_full_path = os.path.join(cwd, mhyph_path)
    with open(mhyph_full_path, 'r') as fin:
        entries_dict = {}
        lines = fin.readlines()
        for line in lines:
            # Only use single words
            if ' ' in line or '-' in line:
                continue
            line = line.strip()
            syllables = line.split('\xa5')
            spelling = ''.join(syllables)
            entries_dict[spelling] = syllables
        words = sorted([entry for entry in entries_dict])
        entries = [(word, entries_dict[word]) for word in words]
        if filt == 'Austen':
            filter_words = austen_words()
            entries = [(entry[0], entry[1]) for entry in entries
                       if entry[0] in filter_words]
    return entries


def austen_words():
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    emma_tokenized = nltk.corpus.gutenberg.words('austen-emma.txt')
    emma_words = set([token.lower() for token in emma_tokenized])
    return emma_words
