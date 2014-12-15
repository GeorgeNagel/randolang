"""Generate vacant, pronouncable domain names."""
from socket import error as socket_error
from time import sleep

import pythonwhois

from randolang import entries_from_cmudict, entries_from_mhyph
from markov import generate_new_sequence, generate_markov_tree
from phones_to_word import phones_to_word

PHONES_METHOD = 'phones_method'
SYLLABLES_METHOD = 'syllables_method'

DOMAINS_TO_GENERATE = 100
MAX_SEQUENCE_SIZE = 100
ORDER = 1

method = SYLLABLES_METHOD

print "Generating Markov tree."
if method == PHONES_METHOD:
    cmu_entries = entries_from_cmudict(filt='Austen')
    sequences = [phones for word, phones in cmu_entries]
    markov_tree = generate_markov_tree(sequences, order=ORDER)
elif method == SYLLABLES_METHOD:
    mhyph_entries = entries_from_mhyph(filt='Austen')
    markov_tree = generate_markov_tree(mhyph_entries, order=ORDER)
print "Done generating Markov tree."

available_domains = []

while len(available_domains) < DOMAINS_TO_GENERATE:
    new_sequence = generate_new_sequence(markov_tree, MAX_SEQUENCE_SIZE)
    if method == PHONES_METHOD:
        word = phones_to_word(new_sequence)
    elif method == SYLLABLES_METHOD:
        word = ''.join(new_sequence)
    domain = "%s.com" % word
    try:
        # Check the whois to see if the domain is taken
        response = pythonwhois.get_whois(domain)
        phrase_to_check = 'No match for "%s"' % domain.upper()
        is_available = phrase_to_check in response['raw'][0]
        if is_available:
            print "%s is available." % domain
            available_domains.append(domain)
        else:
            print "%s is taken." % domain
    except socket_error as e:
        print "Socket error: %s" % e
    # Don't send requests too frequently
    sleep(2)
print "Available domains: %s" % available_domains
