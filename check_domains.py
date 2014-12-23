"""Check domains for generated words.

Usage: python check_domains <cache_name> <tld> <skip_checked>
cache_name - One of 'letters', 'phones', 'syllables', 'tuples'
tld - E.g. '.com'
skip_checked - 0 or 1. Whether or not to re-check already-checked domains.
"""

import sys

from tools.words_cache import WordsCache
from tools.whois_tools import check_domains

if __name__ == '__main__':
    method = sys.argv[1]
    if len(sys.argv) > 2:
        tld = sys.argv[2]
    else:
        tld = '.com'
    if len(sys.argv) > 3:
        skip_checked = bool(int(sys.argv[3]))
    else:
        skip_checked = True
    words_cache = WordsCache()
    words_cache.load_all_caches()
    check_domains(words_cache, method, tld, skip_checked)
    words_cache.save_all_caches()
