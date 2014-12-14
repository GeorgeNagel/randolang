from randolang import (
    generate_new_sequence, generate_markov_tree, entries_from_cmudict,
    entries_from_mhyph
)
from phones_to_word import phones_to_word

WORDS_TO_GENERATE = 1000
MAX_TRANSITIONS = 100
ORDER = 1
method = 'mhyph'

if method == 'cmu':
    cmu_entries = entries_from_cmudict(filt='Austen')
    print "Generating transitions dict."
    sequences = [phones for word,phones in cmu_entries]
    markov_tree = generate_markov_tree(sequences, order=ORDER)
    print "Done generating transitions dict."
elif method == 'mhyph':
    mhyph_entries = entries_from_mhyph(filt='Austen')
    markov_tree = generate_markov_tree(mhyph_entries, order=ORDER)

new_sequences = []
for i in range(WORDS_TO_GENERATE):
    new_sequence = generate_new_sequence(markov_tree, MAX_TRANSITIONS)
    new_sequences.append(new_sequence)

if method == 'cmu':
    words = [phones_to_word(phones) for phones in new_sequences]
elif method == 'mhyph':
    words = [''.join(syllables) for syllables in new_sequences]

story = ' '.join(words)
print "%s" % story
