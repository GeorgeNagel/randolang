# Generate random English-sounding words.

## How it works
A Markov chain of phonemes (small vocal sound unites) is built up based on a small (approximately 7000 words) English dictionary. New words are generated using the phonetic Markov chain and finally spelled out using a rudimentary spelling algorithm.

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
```
$ venv/bin/python generate_words.py
```
## Example output
```
camaturd hezan inturvan icnicstrand plansurnd survabal gry thred langgwin danst nieser groanouns ouurs injoias pocat opurting wands reezortelthy yooth rits sivly saltid galaty laim soal icseptoonatray erats turmantractiv consoal haitrabal questamp rejointaching yeeld residurs affer gaining reelaits sassenid beging hoalsamnattees counsaland wonas trabal cords pravodow recning pains saloot shrabal win acs inclooding ragreefly pradasseed coshan sam atrictaishan medad alied midst ricorsaw hiematly mesier licly cofy proovs dispurd icspurswasian dispursians pacing laf increashean wurs inventid enlorge taibal equiattees periting top stacs sacsensistraind ord hedan shoaldid wok ap lam ocyalaits
```
## TODO
1. Improved spelling going from sounds to spelling in new words is hard. It's hard even in existing words.
2. Allow different languages as inputs. Enable sliders so that fake words sound more like Latin versus more like German.
