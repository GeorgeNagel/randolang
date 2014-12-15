from unittest import TestCase

from randolang import (
    entries_from_cmudict, entries_from_mhyph, austen_words)


class EntriesTest(TestCase):
    def test_entries_from_cmudict(self):
        entries = entries_from_cmudict()
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a.', [u'EY1'])]
        )

    def test_filtered_cmu_entries(self):
        entries = entries_from_cmudict(filt='Austen')
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a', [u'EY1'])]
        )

    def test_mhyph_entries(self):
        entries = entries_from_mhyph()
        self.assertEqual(
            entries[:2],
            [['Aa', 'chen'], ['Aal', 'borg']]
        )

    def test_mhyph_filtered(self):
        entries = entries_from_mhyph(filt='Austen')
        self.assertEqual(
            entries[:2],
            [['ab', 'bey'], ['ab', 'hor']]
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
