from unittest import TestCase

from randolang import generate_words
from tools.words_cache import WordsCache


class TestGenerateWords(TestCase):
    def test_generate_words_tuples(self):
        words_cache = WordsCache()
        words_cache = generate_words(
            number_of_words=2, method='tuples', words_cache=words_cache
        )
        words_cache = generate_words(
            number_of_words=2, method='syllables', words_cache=words_cache
        )
        words_cache = generate_words(
            number_of_words=2, method='phones', words_cache=words_cache
        )
        words_cache = generate_words(
            number_of_words=2, method='letters', words_cache=words_cache
        )
        tuples_dict = words_cache.get_words('tuples')
        self.assertEqual(len(tuples_dict.keys()), 2)
        syllables_dict = words_cache.get_words('syllables')
        self.assertEqual(len(syllables_dict.keys()), 2)
        phones_dict = words_cache.get_words('phones')
        self.assertEqual(len(phones_dict.keys()), 2)
        letters_dict = words_cache.get_words('letters')
        self.assertEqual(len(letters_dict.keys()), 2)
