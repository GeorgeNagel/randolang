from socket import error as socket_error

import pythonwhois
from pythonwhois.shared import WhoisException

from tools.words_cache import AVAILABLE, UNAVAILABLE, UNKNOWN


def check_domains(words_cache, method, tld, skip_checked=True):
    words = words_cache.get_words(method)
    for word in words:
        # Skip if the domain has already been checked
        if tld in words[word] and words[word][tld] in [AVAILABLE, UNAVAILABLE]:
            if skip_checked:
                continue
        domain = '%s%s' % (word, tld)
        availability = domain_availability(domain)
        print "Domain: %s. Availability: %s" % (domain, availability)
        words_cache.add_word(method, word, tld=tld, availability=availability)
    words_cache.save_all_caches()


def domain_availability(domain):
    try:
        response = pythonwhois.get_whois(domain)
        phrase_to_check = 'No match for "%s"' % domain.upper()
        is_available = phrase_to_check in response['raw'][0]
        if is_available:
            availability = AVAILABLE
        else:
            availability = UNAVAILABLE
    except (socket_error, UnicodeDecodeError, WhoisException) as e:
        print "Whois error while checking %s: %s" % (domain, e)
        availability = UNKNOWN
    return availability
