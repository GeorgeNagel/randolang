"""Cache already-generated words and domains."""
import csv
import os

ROOT_CACHE_PATH = 'data/saved_words'

# Domain status values
AVAILABLE = 'available'
UNAVAILABLE = 'unavailable'
UNKNOWN = 'unknown'


class WordsCache(object):
    _words_cache = None
    _domains_cache = None

    def __init__(self):
        # Cache of words and associated domain info
        # Format:
        # {
        #     'phones': {
        #         'jamaska': {
        #             '.com': AVAILABLE
        #         }
        #     },
        #     'syllables': {
        #         'bopperson': {
        #             '.com': UNKNOWN
        #         }
        #     }
        # }
        self._cache = {}

    def get_words(self, cache_name):
        return self._cache.get(cache_name, {})

    def add_word(self, cache_name, word, tld='.com', status=UNKNOWN):
        """Adds a word to the cache.
        cache_name - Scheme used to generate word.
            One of 'tuples', 'syllables', 'phones'
        word - The generated word.
        tld - TLD, e.g. '.com'
        status - Domain availability status.
            One of AVAILABLE, UNAVAILABLE, UNKNOWN
        """
        cache = self._cache.get(cache_name, {})
        domain_dict = cache.get(word, {})
        domain_dict[tld] = status
        cache[word] = domain_dict
        self._cache[cache_name] = cache

    def save_all_caches(self):
        """Save all of the generated words to file."""
        self._save_cache('phones')
        self._save_cache('tuples')
        self._save_cache('syllables')

    def _save_cache(self, cache_name):
        """Write the cache as a csv file."""
        dir_name = os.path.join(ROOT_CACHE_PATH, cache_name)
        headers = ['Word', 'TLD', 'Availability']
        cache = self._cache.get(cache_name, {})
        rows = [headers]
        for word in cache:
            for tld in cache[word]:
                availability = cache[word][tld]
                row = [word, tld, availability]
                rows.append(row)
        rows = sorted(rows)
        file_path = os.path.join(dir_name, 'words.csv')
        with open(file_path, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerows(rows)

    def load_all_caches(self):
        """Load all of the generated words from file."""
        self._load_cache('phones')
        self._load_cache('tuples')
        self._load_cache('syllables')

    def _load_cache(self, cache_name):
        dir_name = os.path.join(ROOT_CACHE_PATH, cache_name)
        file_path = os.path.join(dir_name, 'words.csv')
        # Open the words file, create it if it doesn't exist
        rows = []
        with open(file_path, 'w+') as fin:
            reader = csv.reader(fin)
            rows = [row for row in reader]
        # Skip the header row
        for row in rows[1:]:
            word, tld, availability = row
            self.add_word(cache_name, word, tld=tld, status=availability)
