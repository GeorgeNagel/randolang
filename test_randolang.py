from unittest import TestCase

from randolang import (
    _handle_short_vowels, generate_transitions, _clean_phone,
    generate_transitions_dict, add_transition_to_dict,
    order_from_transitions_dict, generate_word, _generate_phone,
    entries_from_cmudict, austen_words, phones_to_word,
    _protect_short_vowels, _handle_long_vowels, _handle_c,
    _handle_q, _handle_jh, _handle_hh, _handle_dh)


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


class TestGenerateTransitions(TestCase):
    def test_first_order_transitions(self):
        phones = ['K0', 'UH1', 'T0']
        transitions = generate_transitions(phones)
        self.assertEqual(
            transitions,
            [
                ['START', 'K'],
                ['K', 'UH'],
                ['UH', 'T'],
                ['T', 'STOP']
            ]
        )
    def test_second_order_transitions(self):
        phones = ['K', 'UH', 'T']
        transitions = generate_transitions(phones, order=2)
        self.assertEqual(
            transitions,
            [
                ['START', 'START', 'K'],
                ['START', 'K', 'UH'],
                ['K', 'UH', 'T'],
                ['UH', 'T', 'STOP'],
                ['T', 'STOP', 'STOP']
            ]
        )

class TestCleanPhone(TestCase):
    def test_clean_phone(self):
        phone = 'AA1'
        cleaned_phone = _clean_phone(phone)
        self.assertEqual(cleaned_phone, 'AA')

class TestGenerateTransitionsDict(TestCase):
    def setUp(self):
        self.entries = [
            ('booboo', ['B0', 'UW1', 'B', 'UW1'])
        ]

    def test_generate_transitions_dict(self):
        transitions_dict = generate_transitions_dict(self.entries, order=1)
        self.assertEqual(
            transitions_dict,
            {
                'START': {
                    'B': 1
                },
                'B': {
                    'UW': 2
                },
                'UW': {
                    'B': 1,
                    'STOP': 1
                }
            }
        )

    def test_second_order(self):
        transitions_dict = generate_transitions_dict(self.entries, order=2)
        self.assertEqual(
            transitions_dict,
            {
                'START': {
                    'START': {
                        'B': 1
                    },
                    'B': {
                        'UW': 1,
                    }
                },
                'B': {
                    'UW': {
                        'B': 1,
                        'STOP': 1
                    }
                },
                'UW': {
                    'B': {
                        'UW': 1
                    },
                    'STOP': {
                        'STOP': 1
                    }
                }
            }
        )

class AddTransitionTestCase(TestCase):
    def test_add_first_order(self):
        transition = ('B', 'UW')
        transitions_dict = {
            'B': {
                'AH': 1
            }
        }
        add_transition_to_dict(transitions_dict, transition)
        self.assertEqual(
            transitions_dict,
            {
                'B': {
                    'AH': 1,
                    'UW': 1
                }
            }
        )

    def test_add_second_order(self):
        transition = ('B', 'UW', 'K')
        transitions_dict = {
            'B': {
                'AH': {
                    'T': 1
                }
            }
        }
        add_transition_to_dict(transitions_dict, transition)
        self.assertEqual(
            transitions_dict,
            {
                'B': {
                    'AH': {
                        'T': 1
                    },
                    'UW': {
                        'K': 1
                    }
                }
            }
        )

class OrderFromTransitionsDictTest(TestCase):
    def test_first_order_transitions_dict(self):
        transitions_dict = {
            'B': {
                'AH': 1
            }
        }
        order = order_from_transitions_dict(transitions_dict)
        self.assertEqual(order, 1)

    def test_second_order_transitions_dict(self):
        transitions_dict = {
            'B': {
                'UH': {
                    'B': 1
                }
            }
        }
        order = order_from_transitions_dict(transitions_dict)
        self.assertEqual(order, 2)

class GenerateWordTest(TestCase):
    def test_first_order_word(self):
        transitions_dict = {
            'START': {
                'B': 1
            },
            'B': {
                'UH': 1
            },
            'UH': {
                'STOP': 1
            }
        }
        word = generate_word(transitions_dict, 10)
        self.assertEqual(word, 'bu')

    def test_long_word_cutoff(self):
        transitions_dict = {
            'START': {
                'B': 1
            },
            'B': {
                'UH': 1
            },
            'UH': {
                'L': 1
            },
            'L': {
                'STOP': 1
            }
        }
        word = generate_word(transitions_dict, 1)
        self.assertEqual(word, 'b')

    def test_second_order_word(self):
        transitions_dict = {
            'START': {
                'START': {
                    'B': 1
                },
                'B': {
                    'UH': 1
                }
            },
            'B': {
                'UH': {
                    'STOP': 1
                }
            },
            'UH': {
                'STOP': {
                    'STOP': 1
                }
            }
        }
        word = generate_word(transitions_dict, 10)
        self.assertEqual(word, 'bu')

class GeneratePhonemeTest(TestCase):
    def test_generate_phoneme(self):
        prior_phones = ['START', 'START']
        transitions_dict = {
            'START': {
                'START': {
                    'B': 1
                }
            }
        }
        phone = _generate_phone(transitions_dict, prior_phones)
        self.assertEqual(phone, 'B')

class EntriesTest(TestCase):
    def test_entries_from_cmudict(self):
        entries = entries_from_cmudict()
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a.', [u'EY1'])]
        )

    def test_filtered_entries(self):
        entries = entries_from_cmudict(filt='Austen')
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a', [u'EY1'])]
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