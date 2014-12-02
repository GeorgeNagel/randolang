from randolang import generate_word, generate_transitions_dict, entries_from_cmudict

WORDS_TO_GENERATE = 1000
MAX_PHONE_SIZE = 100
ORDER = 3

cmu_entries = entries_from_cmudict(filt='Austen')


print "Generating transitions dict."
transitions_dict = generate_transitions_dict(cmu_entries, order=ORDER)
print "Done generating transitions dict."

words = []
for i in range(WORDS_TO_GENERATE):
    word = generate_word(transitions_dict, MAX_PHONE_SIZE)
    words.append(word)

story = ' '.join(words)
print "%s" % story
