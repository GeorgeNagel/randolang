from randolang import (
    generate_new_sequence, generate_markov_tree, entries_from_cmudict,
    entries_from_mhyph
)
from phones_to_word import phones_to_word

PHONES_METHOD = 'phones_method'
SYLLABLES_METHOD = 'syllables_method'

WORDS_TO_GENERATE = 1000
MAX_TRANSITIONS = 100
ORDER = 1
method = SYLLABLES_METHOD


print "Generating Markov tree."
if method == PHONES_METHOD:
    cmu_entries = entries_from_cmudict(filt='Austen')
    sequences = [phones for word,phones in cmu_entries]
    markov_tree = generate_markov_tree(sequences, order=ORDER)
elif method == SYLLABLES_METHOD:
    mhyph_entries = entries_from_mhyph(filt='Austen')
    markov_tree = generate_markov_tree(mhyph_entries, order=ORDER)
print "Done generating Markov tree."

new_sequences = []
for i in range(WORDS_TO_GENERATE):
    new_sequence = generate_new_sequence(markov_tree, MAX_TRANSITIONS)
    new_sequences.append(new_sequence)

if method == PHONES_METHOD:
    words = [phones_to_word(phones) for phones in new_sequences]
elif method == SYLLABLES_METHOD:
    words = [''.join(syllables) for syllables in new_sequences]

story = ' '.join(words)
print "%s" % story
