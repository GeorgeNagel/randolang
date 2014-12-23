# Generate new English-like words.

## How it works
A small (approximately 7000 words) English dictionary is broken down into units (letters, phones, or syllables) and a Markov process is used to generate new words. When using phones as the word unit, a rudimentary spelling algorithm is used to create English-pronouncable words.

## Set up the python environment.
```
$ git clone https://github.com/GeorgeNagel/randolang
$ cd randolang
# Create the python virtual environment
$ virtualenv venv
# Install the project requirements
$ source venv/bin/activate
$ pip install -r requirements.txt
```
## Run the test suite
```
$ venv/bin/nosetests
```
## Generate some random words
There are several methods to create new words. Three methods use a Markov process using different building blocks: letters, phones, and syllables. A fourth method, tuples, creates new words by randomly combining existing words.

Usage: ```venv/bin/python generate_words.py <method> <number of words> <order>``` where order is the order of the markov process. When using the 'words' method, order is the number of words to combine.

```
$ venv/bin/python generate_words.py syllables 100 2
Number of words: 100. Method: syllables. Order: 2
Generating words...
New word: subjectionable
New word: stipulative
...
New word: preparagus
Done
```
Words are also saved in a .csv file in data/saved_words.

## Check for available domains
You can check the availability of domains using these new words with the usage: ```venv/bin/python check_domains.py <method> <tld> <skip_checked>```. When skip_checked is '0', domains which were already checked according to the relevant .csv file will be checked again. 

```
$ venv/bin/python check_domains.py syllables .com 1
Domain: emony.com. Availability: unavailable
Domain: inabilious.com. Availability: available
...
Domain: perfectionately.com. Availability: available
```
This will update the relevant csv file in data/saved_words.


## TODO
1. Improved spelling when using the 'phones' method. Spelling from phones in new words is hard. It's hard even in existing words.
2. Allow different languages as inputs so that fake words sound more like Latin versus more like German.

## Sources
This project uses a few freely-available sources.
1. mhyph (http://www.gutenberg.org/ebooks/3204) for a list of syllabified English words.
2. CMUDict via nltk (http://www.nltk.org/_modules/nltk/corpus/reader/cmudict.html) for a list of pronunciations of English words.
3. Jane Austen's Emma via nltk (http://www.gutenberg.org/ebooks/158) for a sane list of common English words.
