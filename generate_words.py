import sys

from randolang import generate_words
from tools.words_cache import WordsCache

if __name__ == '__main__':
    number_of_words = int(sys.argv[1])
    method = sys.argv[2]
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
