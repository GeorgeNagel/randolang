import pythonwhois


def domain_is_available(domain):
    response = pythonwhois.get_whois(domain)
    phrase_to_check = 'No match for "%s"' % domain.upper()
    is_available = phrase_to_check in response['raw'][0]
    return is_available
