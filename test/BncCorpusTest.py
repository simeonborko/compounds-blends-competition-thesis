import time

import sys

from tools.en.corpus.SessionBncCorpus import SessionBncCorpus
from tools.en.corpus.BasicBncCorpus import BasicBncCorpus
from tools.en.corpus.UrlLibBncCorpus import UrlLibBncCorpus

clss = [UrlLibBncCorpus, BasicBncCorpus, SessionBncCorpus]

with open('100-words.txt') as fp:
    words = [x.strip() for x in fp][:25]

print(words)


for cls in clss:
    print(cls)
    for i in range(3):
        print("Test", i+1)
        a = time.time()

        corpus = cls()
        for word in words:
            f = corpus.get_frequency(word)
            print(word, f, file=sys.stderr, sep='\t')

        b = time.time()
        print(b - a)





