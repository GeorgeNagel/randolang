from collections import defaultdict
import random
import os

import nltk

cwd = os.getcwd()
data_dir = 'data'
data_path = os.path.join(cwd, data_dir)
print data_path
nltk.data.path = [data_path]

entries = nltk.corpus.cmudict.entries()
print type(nltk.corpus.cmudict)

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

# # 
# print len(entries)
# for entry in entries:
#     # print entry
#     word, pron_list = entry
#     clean_pron_list = [pron.strip('0123456789') for pron in pron_list]
#     translated_pron_list = [conversions[pron] for pron in clean_pron_list]
#     joined_pron = ''.join(translated_pron_list)
#     # print 'Word: %s. Trans: %s' % (word, joined_pron)

def _generate_transitions(pron_list):
    """Takes a list of pronunciation phonemes and generates a list of transitions.
    The transitions are to be used as keys in the markov dict.
    """
    padded_pron_list = ['START'] + pron_list + ['STOP']
    transitions = []
    for index, pron in enumerate(padded_pron_list[:-1]):
        first_phoneme = pron.strip('0123456789')
        second_phoneme = padded_pron_list[index+1].strip('0123456789')
        transition = (first_phoneme, second_phoneme)
        transitions.append(transition)
    return transitions

short_entries_list = entries
transitions_dict = {}
number_transitions = 0
for entry in short_entries_list:
    word, pron_list = entry
    transitions = _generate_transitions(pron_list)
    number_transitions += 1
    for transition in transitions:
        first_phoneme, second_phoneme = transition
        if first_phoneme  not in transitions_dict:
            transitions_dict[first_phoneme] = defaultdict(int)
        transitions_dict[first_phoneme][second_phoneme] += 1


def generate_word_normal():
    # generate words based on assumed normal distributions of phonemes
    current_phoneme = 'START'
    phones = []
    iters = 0
    next_phoneme = ''
    while next_phoneme != 'STOP' and iters <= 10:
        iters +=1
        phones.append(current_phoneme)
        possible_nexts = transitions_dict[current_phoneme].keys()
        next_phoneme = random.choice(possible_nexts)
        current_phoneme = next_phoneme

    phones = phones[1:]
    novel_word = ''.join(phones)
    return novel_word

def generate_word_pdf():
    # generate words based on the pdf of phoneme transitions
    current_phoneme = 'START'
    phones = []
    iters = 0
    next_phoneme = ''
    while next_phoneme != 'STOP' and iters <= 10:
        iters +=1
        phones.append(current_phoneme)
        # Generate the possible transitions using the transitions dict
        # values as the pdf.
        possible_nexts = []
        for next_phoneme in transitions_dict[current_phoneme]:
            number_of_appearances = transitions_dict[current_phoneme][next_phoneme]
            nexts = [next_phoneme]*number_of_appearances
            possible_nexts.extend(nexts)
        next_phoneme = random.choice(possible_nexts)
        current_phoneme = next_phoneme

    phones = phones[1:]
    novel_word = ''.join(phones)
    return novel_word


print "Transitions dict: %s" % transitions_dict

number_of_words = 10
for i in range(number_of_words):
    word = generate_word_pdf()
    print "Novel word: %s" % word
