from unittest import TestCase

from word_data import (
    entries_from_cmudict, entries_from_mhyph, austen_words, filter_entries)


class EntriesTest(TestCase):
    def test_entries_from_cmudict(self):
        entries = entries_from_cmudict()
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a.', [u'EY1'])]
        )

    def test_filtered_cmu_entries(self):
        entries = entries_from_cmudict()
        entries = filter_entries(entries, 'Austen')
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a', [u'EY1'])]
        )

    def test_mhyph_entries(self):
        entries = entries_from_mhyph()
        self.assertEqual(
            entries[:2],
            [('aa', ['a', 'a']), ('aachen', ['aa', 'chen'])]
        )

    def test_mhyph_filtered(self):
        entries = entries_from_mhyph()
        entries = filter_entries(entries, 'Austen')
        self.assertEqual(
            entries[:2],
            [('abbey', ['ab', 'bey']), ('abhor', ['ab', 'hor'])]
        )


class AustenWordsTest(TestCase):
    def test_austen_words(self):
        words = [word for word in austen_words()]
        words = sorted(words)[-10:]
        self.assertEqual(
            words,
            [
                u'young', u'younger', u'youngest',
                u'your', u'yours', u'yourself', u'youth',
                u'youthful', u'zeal', u'zigzags'
            ]
        )
