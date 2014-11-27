from randolang import generate_word_pdf, generate_transitions_dict, entries_from_cmudict

WORDS_TO_GENERATE = 100
ORDER = 1

cmu_entries = entries_from_cmudict()

print "Generating transitions dict."
transitions_dict = generate_transitions_dict(cmu_entries, order=ORDER)
print "Done generating transitions dict."

for i in range(WORDS_TO_GENERATE):
    word = generate_word_pdf(transitions_dict)
    print "Word: %s" % word
