from randolang import generate_words


words = generate_words(method='syllables', order=1, number_of_words=100)

story = ' '.join(words)
print "%s" % story
