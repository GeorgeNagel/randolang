from unittest import TestCase

from phones_to_word import (
    _handle_short_vowels, phones_to_word,
    _protect_short_vowels, _handle_long_vowels, _handle_c,
    _handle_q, _handle_jh, _handle_hh, _handle_dh)
from randolang import entries_from_cmudict, _clean_phone


class TestPhonesToWord(TestCase):
    def test_phones_to_words(self):
        phones = ['AE', 'T']
        word = phones_to_word(phones)
        self.assertEqual(word, 'at')

        phones = ['AE', 'K', 'W', 'IH', 'T']
        word = phones_to_word(phones)
        self.assertEqual(word, 'aquit')

        phones = ['K', 'EY', 'JH']
        word = phones_to_word(phones)
        self.assertEqual(word, 'cage')

        phones = ['H', 'AH', 'T']
        word = phones_to_word(phones)
        self.assertEqual(word, 'het')

    def test_words_correct(self):
        """Test the accuracy of the spelling against known words."""
        entries = entries_from_cmudict(filt="Austen")
        number_correct = 774
        total_words = len(entries)
        for entry in entries:
            word, phones = entry
            cleaned_phones = [_clean_phone(phone) for phone in phones]
            calculated_word = phones_to_word(cleaned_phones)
            if word == calculated_word:
                number_correct += 1
            else:
                print "Incorrect spelling. Expected %s, got %s." % (word, calculated_word)
        self.assertEqual(number_correct, 1637)

    def test_protect_short_vowels(self):
        phones = ['B', 'IH', 'T', 'ER']
        phones_protected = _protect_short_vowels(phones)
        self.assertEqual(phones_protected, ['B', 'IH', 'tt', 'ER'])

        # Don't double when two consonants are next to each other
        phones = ['IH', 'N', 'K']
        phones_protected = _protect_short_vowels(phones)
        self.assertEqual(phones_protected, ['IH', 'N', 'K'])

        # Don't double when there's no following vowel
        phones = ['F', 'EH', 'N']
        phones_protected = _protect_short_vowels(phones)
        self.assertEqual(phones_protected, ['F', 'EH', 'N'])

        # Don't double DH
        phones = ['P', 'UH', 'DH', 'IY']
        phones_protected = _protect_short_vowels(phones)
        self.assertEqual(phones_protected, ['P', 'UH', 'DH', 'IY'])


    def test_handle_short_vowels(self):
        # Short A
        phones = ['AE', 'T']
        short_replaced = _handle_short_vowels(phones)
        self.assertEqual(short_replaced, ['a', 'T'])

        # Short E
        phones = ['R', 'EH', 'D']
        short_replaced = _handle_short_vowels(phones)
        self.assertEqual(short_replaced, ['R', 'e', 'D'])

        # Short I
        phones = ['IH', 'T']
        short_replaced = _handle_short_vowels(phones)
        self.assertEqual(short_replaced, ['i', 'T'])

        # Short O
        phones = ['AA', 'D']
        short_replaced = _handle_short_vowels(phones)
        self.assertEqual(short_replaced, ['o', 'D'])

        # Aught sound
        phones = ['T', 'AO', 'T']
        short_replaced = _handle_short_vowels(phones)
        self.assertEqual(short_replaced, ['T', 'o', 'T'])

        # Short U
        phones = ['AH', 'P']
        short_replaced = _handle_short_vowels(phones)
        self.assertEqual(short_replaced, ['e', 'P'])

    def test_handle_long_vowels(self):
        # Start of word cases
        phones = ['EY', 'P', 'u', 'L', 'i', 'T', 'i', 'K', 'u', 'L']
        long_replaced = _handle_long_vowels(phones)
        self.assertEqual(
            long_replaced,
            ['a', 'P', 'u', 'L', 'i', 'T', 'i', 'K', 'u', 'L']
        )

        # Intermediate cases
        phones = ['F', 'L', 'IY', 'S', 'IH', 'Z']
        long_replaced = _handle_long_vowels(phones)
        self.assertEqual(
            long_replaced,
            ['F', 'L', 'ee', 'S', 'IH', 'Z']
        )

        # Before last consonant cases
        phones = ['D', 'EY', 'T']
        long_replaced = _handle_long_vowels(phones)
        self.assertEqual(
            long_replaced,
            ['D', 'a', 'T', 'e']
        )

        phones = ['D', 'EY', 'T', 'S']
        long_replaced = _handle_long_vowels(phones)
        self.assertEqual(
            long_replaced,
            ['D', 'a', 'T', 'e', 'S']
        )

        # End of word cases
        phones = ['D', 'IH', 'L', 'EY']
        long_replaced = _handle_long_vowels(phones)
        self.assertEqual(
            long_replaced,
            ['D', 'IH', 'L', 'ay']
        )

        # Short word
        phones = ['EY', 'M']
        long_replaced = _handle_long_vowels(phones)
        self.assertEqual(
            long_replaced,
            ['a', 'M']
        )

        # Three consonants in a row
        phones = ['S', 'K', 'OW', 'L', 'D', 'Z']
        long_replaced = _handle_long_vowels(phones)
        self.assertEqual(
            long_replaced,
            ['S', 'K', 'o', 'L', 'D', 'Z']
        )

    def test_handle_c(self):
        # Use cc to protect short vowel
        phones = ['S', 'T', 'u', 'kk', 'OW']
        c_replaced = _handle_c(phones)
        self.assertEqual(c_replaced, ['S', 'T', 'u', 'cc', 'OW'])

        # Use k when followed by e i or y
        phones = ['K', 'i', 'N']
        c_replaced = _handle_c(phones)
        self.assertEqual(c_replaced, ['k', 'i', 'N'])

        phones = ['M', 'a', 'K', 'e']
        c_replaced = _handle_c(phones)
        self.assertEqual(c_replaced, ['M', 'a', 'k', 'e'])

        # ck follows short vowel at the end of word
        phones = ['T', 'R', 'i', 'K']
        c_replaced = _handle_c(phones)
        self.assertEqual(c_replaced, ['T', 'R', 'i', 'ck'])

        # Fall back to C
        phones = ['K', 'a', 'T']
        c_replaced = _handle_c(phones)
        self.assertEqual(c_replaced, ['c', 'a', 'T'])

    def test_handle_q(self):
        phones = ['a', 'K', 'W', 'i', 'er']
        q_replaced = _handle_q(phones)
        self.assertEqual(q_replaced, ['a', 'qu', 'i', 'er'])

    def test_handle_jh(self):
        phones = ['AH', 'N', 'JH', 'AH', 'S', 'T']
        jh_replaced = _handle_jh(phones)
        self.assertEqual(jh_replaced, ['AH', 'N', 'j', 'AH', 'S', 'T'])

        phones = ['EY', 'JH']
        jh_replaced = _handle_jh(phones)
        self.assertEqual(jh_replaced, ['EY', 'g'])

    def test_handle_hh(self):
        phones = ['HH', 'AH', 'T']
        hh_replaced = _handle_hh(phones)
        self.assertEqual(hh_replaced, ['h', 'AH', 'T'])

    def test_handle_dh(self):
        phones = ['W', 'ER', 'DH', 'IY']
        dh_replaced = _handle_dh(phones)
        self.assertEqual(dh_replaced, ['W', 'ER', 'th', 'IY'])