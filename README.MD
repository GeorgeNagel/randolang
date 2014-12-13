# Generate random english-sounding words.

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
