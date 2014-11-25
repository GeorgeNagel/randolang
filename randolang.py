import os

import nltk

cwd = os.getcwd()
data_dir = 'data'
data_path = os.path.join(cwd, data_dir)
print data_path
nltk.data.path = [data_path]

entries = nltk.corpus.cmudict.entries()
print type(nltk.corpus.cmudict)

print len(entries)
for entry in entries[:10]:
	print entry

