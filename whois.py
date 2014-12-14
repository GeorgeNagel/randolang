"""Generate vacant, pronouncable domain names."""
from socket import error as socket_error

import pythonwhois

from randolang import generate_word, generate_transitions_dict, entries_from_cmudict

DOMAINS_TO_GENERATE = 100
MAX_PHONE_SIZE = 100
ORDER = 3

cmu_entries = entries_from_cmudict(filt='Austen')
print "Generating transitions dict."
transitions_dict = generate_transitions_dict(cmu_entries, order=ORDER)
print "Done generating transitions dict."

available_domains = []

while len(available_domains) < DOMAINS_TO_GENERATE:
    random_word = generate_word(transitions_dict, MAX_PHONE_SIZE)
    domain = "%s.com" % random_word
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

print "Available domains: %s" % available_domains