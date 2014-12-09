from unittest import TestCase

from phones_to_word import phones_to_word
from randolang import entries_from_cmudict, _clean_phones


class TestPhonesToWord(TestCase):
    def test_phones_to_word(self):
        cases = [
            (['B', 'IH', 'D'], ['bihd'])
        ]
        for case in cases:
            phones, spellings = case
            calculated_word = phones_to_word(phones)
            self.assertIn(calculated_word, spellings)

    def test_words_correct(self):
        """Test the accuracy of the spelling against known words."""
        entries = entries_from_cmudict(filt="Austen")
        number_correct = 0
        total_words = len(entries)
        for entry in entries:
            word, phones = entry
            # clean_phone modifies phones in-place, so
            cleaned_phones = _clean_phones(phones)
            calculated_word = phones_to_word(cleaned_phones)
            if word == calculated_word:
                number_correct += 1
            else:
                print "Incorrect spelling. Expected %s, got %s. Phones: %s" % (word, calculated_word, phones)
        self.assertEqual(number_correct, 24)
