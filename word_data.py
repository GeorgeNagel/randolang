import os

import nltk


def entries_from_cmudict():
    """Create a list of entries from the cmu corpus.
    If filt='Austen', only uses words that appear in Jane Austen's Emma.
    """
    cwd = os.getcwd()
    data_dir = 'data'
    data_path = os.path.join(cwd, data_dir)
    nltk.data.path = [data_path]
    entries = nltk.corpus.cmudict.entries()
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
            line = line.strip().lower()
            syllables = line.split('\xa5')
            spelling = ''.join(syllables)
            entries_dict[spelling] = syllables
        words = sorted([entry for entry in entries_dict])
        entries = [(word, entries_dict[word]) for word in words]
    return entries


def filter_entries(entries, filt):
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
