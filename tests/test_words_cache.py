from unittest import TestCase
import os

from mock import mock_open, patch, call

from tools.words_cache import WordsCache, AVAILABLE


class TestWordsCache(TestCase):
    def test_add_word(self):
        words_cache = WordsCache()
        words_cache.add_word(
            'syllables', 'bungle', tld='.net', status=AVAILABLE
        )
        self.assertEqual(
            words_cache._cache,
            {
                'syllables': {
                    'bungle': {
                        '.net': 'available'
                    }
                }
            }
        )

    def test_save_cache(self):
        m = mock_open()
        with patch('tools.words_cache.open', m, create=True):
            words_cache = WordsCache()
            words_cache.add_word(
                'tuples', 'tripance'
            )
            words_cache.save_all_caches()
        self.assertEqual(
            m.mock_calls,
            [
                call('data/saved_words/phones/words.csv', 'w'),
                call().__enter__(),
                call().write('Word,TLD,Availability\r\n'),
                call().__exit__(None, None, None),
                call('data/saved_words/tuples/words.csv', 'w'),
                call().__enter__(),
                call().write('Word,TLD,Availability\r\n'),
                call().write('tripance,.com,unknown\r\n'),
                call().__exit__(None, None, None),
                call('data/saved_words/syllables/words.csv', 'w'),
                call().__enter__(),
                call().write('Word,TLD,Availability\r\n'),
                call().__exit__(None, None, None)
            ]
        )

    def test_load_cache(self):
        words_cache = WordsCache()
        testing_dir = os.path.dirname(os.path.realpath(__file__))
        words_cache.root_cache_path = os.path.join(
            testing_dir, 'fixtures/data'
        )

        words_cache.load_all_caches()
        self.assertEqual(
            words_cache._cache,
            {'tuples': {'tripance': {'.com': 'unavailable'}}}
        )
