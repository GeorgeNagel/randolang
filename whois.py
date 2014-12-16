"""Generate vacant, pronouncable domain names."""
from socket import error as socket_error
from time import sleep

from randolang import generate_words
from tools.whois_tools import domain_is_available

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
        is_available = domain_is_available(domain)
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
