from unittest import TestCase

from randolang import (
    phones_to_word, generate_transitions, _clean_phone,
    generate_transitions_dict, add_transition_to_dict)


class TestPhonesToWord(TestCase):
    def test_phones_to_word(self):
        phones = ['AA', 'R', 'D', 'V', 'AA', 'R', 'K']
        word = phones_to_word(phones)
        self.assertEqual(word, 'ahrdvahrc')

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