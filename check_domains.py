import sys

from tools.words_cache import WordsCache
from tools.whois_tools import check_domains

if __name__ == '__main__':
    method = sys.argv[1]
    tld = sys.argv[2]
    if len(sys.argv) > 3:
        skip_checked = bool(int(sys.argv[3]))
    else:
        skip_checked = True
    words_cache = WordsCache()
    words_cache.load_all_caches()
    check_domains(words_cache, method, tld, skip_checked)
