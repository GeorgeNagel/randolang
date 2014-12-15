"""Generate vacant, pronouncable domain names."""
from socket import error as socket_error
from time import sleep

import pythonwhois

from randolang import generate_words

DOMAINS_TO_GENERATE = 100

available_domains = []

words = generate_words(method='syllables', order=1, number_of_words=100)

while len(available_domains) < DOMAINS_TO_GENERATE:
    if not words:
        words = generate_words(method='syllables',
                               order=1, number_of_words=100)
    word = words.pop()
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
