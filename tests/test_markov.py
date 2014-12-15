from unittest import TestCase

from markov import (
    generate_transitions,
    generate_markov_tree, add_transition_to_tree,
    order_from_markov_tree, generate_new_sequence, _generate_sequence_element)


class TestGenerateTransitions(TestCase):
    def test_first_order_transitions(self):
        phones = ['K', 'UH', 'T']
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


class TestGenerateMarkovTree(TestCase):
    def setUp(self):
        self.sequences = [
            ['B', 'UW', 'B', 'UW']
        ]

    def test_generate_markov_tree(self):
        transitions_dict = generate_markov_tree(self.sequences, order=1)
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
        transitions_dict = generate_markov_tree(self.sequences, order=2)
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
        markov_tree = {
            'B': {
                'AH': 1
            }
        }
        add_transition_to_tree(markov_tree, transition)
        self.assertEqual(
            markov_tree,
            {
                'B': {
                    'AH': 1,
                    'UW': 1
                }
            }
        )

    def test_add_second_order(self):
        transition = ('B', 'UW', 'K')
        markov_tree = {
            'B': {
                'AH': {
                    'T': 1
                }
            }
        }
        add_transition_to_tree(markov_tree, transition)
        self.assertEqual(
            markov_tree,
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


class OrderFromMarkovTreeTest(TestCase):
    def test_first_order_tree(self):
        markov_tree = {
            'B': {
                'AH': 1
            }
        }
        order = order_from_markov_tree(markov_tree)
        self.assertEqual(order, 1)

    def test_second_order_tree(self):
        markov_tree = {
            'B': {
                'UH': {
                    'B': 1
                }
            }
        }
        order = order_from_markov_tree(markov_tree)
        self.assertEqual(order, 2)


class GenerateSequenceTest(TestCase):
    def test_first_order(self):
        markov_tree = {
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
        sequence = generate_new_sequence(markov_tree, 10)
        self.assertEqual(sequence, ['B', 'UH'])

    def test_cutoff(self):
        markov_tree = {
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
        sequence = generate_new_sequence(markov_tree, 1)
        self.assertEqual(sequence, ['B'])

    def test_second_order(self):
        markov_tree = {
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
        sequence = generate_new_sequence(markov_tree, 10)
        self.assertEqual(sequence, ['B', 'UH'])


class GenerateSequenceElementTest(TestCase):
    def test_generate_sequence_element(self):
        prior_sequence = ['START', 'START']
        markov_tree = {
            'START': {
                'START': {
                    'B': 1
                }
            }
        }
        element = _generate_sequence_element(markov_tree, prior_sequence)
        self.assertEqual(element, 'B')
