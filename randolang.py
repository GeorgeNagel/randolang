import copy
import os

import nltk


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
    if filt is None:
        entries = nltk.corpus.cmudict.entries()
    elif filt == 'Austen':
        entries = nltk.corpus.cmudict.entries()
        filter_words = austen_words()
        filtered_entries = [(entry[0], entry[1]) for entry in entries
                            if entry[0] in filter_words]
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
            spelling = ''.join(syllables)
            entries[spelling] = syllables
        words = sorted([entry for entry in entries])
        if filt == 'Austen':
            filter_words = austen_words()
            sequences = [entries[word] for word in words
                         if word in filter_words]
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
