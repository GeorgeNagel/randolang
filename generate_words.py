"""Generate new words and save them to file.

Usage: python generate_words <method> <number_of_words> <order>
method - One of "tuples", "letters", "syllables", "phones"
number_of_words - The number of new words to generate
order - The order of the markov tree used. When using the 'tuples' method,
    the number of words to join.
"""
import sys

from randolang import generate_words
from tools.words_cache import WordsCache

if __name__ == '__main__':
    method = sys.argv[1]
    if len(sys.argv) < 3:
        number_of_words = 100
    else:
        number_of_words = int(sys.argv[2])
    if len(sys.argv) < 4:
        order = 2
    else:
        order = int(sys.argv[3])
    print "Number of words: %d. Method: %s. Order: %d" % (
        number_of_words, method, order
    )
    print "Generating words..."
    words_cache = WordsCache()
    words_cache.load_all_caches()
    words_cache = generate_words(number_of_words=number_of_words,
                                 order=order,
                                 words_cache=words_cache,
                                 method=method)
    words_cache.save_all_caches()
    print "Done"
