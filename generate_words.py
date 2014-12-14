from randolang import (
    generate_word, generate_markov_tree, entries_from_cmudict,
    entries_from_mhyph
)

WORDS_TO_GENERATE = 1000
MAX_TRANSITIONS = 100
ORDER = 3
method = 'cmu'

if method == 'cmu':
    cmu_entries = entries_from_cmudict(filt='Austen')
    print "Generating transitions dict."
    sequences = [phones for word,phones in cmu_entries]
    transitions_dict = generate_markov_tree(sequences, order=ORDER)
    print "Done generating transitions dict."
elif method == 'mhyph':
    mhyph_entries = entries_from_mhyph(filt='Austen')

words = []
for i in range(WORDS_TO_GENERATE):
    word = generate_word(transitions_dict, MAX_TRANSITIONS)
    words.append(word)

story = ' '.join(words)
print "%s" % story
