"""Generate vacant, pronouncable domain names."""
from socket import error as socket_error
from time import sleep

from pythonwhois.shared import WhoisException

from randolang import generate_words
from tools.whois_tools import domain_is_available

DOMAINS_TO_GENERATE = 100

available_domains = []

unavailable_path = 'data/unavailable.txt'
available_path = 'data/available.txt'

with open(available_path, 'r') as fin:
    avaialble_domains = [line.strip() for line in fin.readlines()]
with open(unavailable_path, 'r') as fin:
    unavailable_domains = [line.strip() for line in fin.readlines()]
checked_domains = available_domains + unavailable_domains

words = generate_words(method='syllables', order=1, number_of_words=100)

while len(available_domains) < DOMAINS_TO_GENERATE:
    if not words:
        words = generate_words(method='syllables',
                               order=1, number_of_words=100)
    word = words.pop()
    domain = "%s.com" % word
    if domain in checked_domains:
        print "Already checked %s. Continuing..." % domain
        continue
    try:
        # Check the whois to see if the domain is taken
        is_available = domain_is_available(domain)
        if is_available:
            print "%s is available." % domain
            available_domains.append(domain)
            with open(available_path, 'a') as fout:
                fout.write("%s\n" % domain)
        else:
            print "%s is taken." % domain
            with open(unavailable_path, 'a') as fout:
                fout.write("%s\n" % domain)
        checked_domains.append(domain)
    except (socket_error, UnicodeDecodeError, WhoisException) as e:
        print "Whois error while checking %s: %s" % (domain, e)
    # Don't send requests too frequently
    sleep(2)
print "Available domains: %s" % available_domains
