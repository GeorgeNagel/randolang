from unittest import TestCase

from randolang import phones_to_word
class TestPhonesToWord(TestCase):
    def test_phones_to_word(self):
        phones = ['AA', 'R', 'D', 'V', 'AA', 'R', 'K']
        word = phones_to_word(phones)
        self.assertEqual(word, 'ahrdvahrc')
