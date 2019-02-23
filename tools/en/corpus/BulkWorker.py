from typing import List, Dict, Set

import sys

from tools.en.corpus.BasicBncCorpus import BasicBncCorpus
from tools.en.corpus.SessionBncCorpus import SessionBncCorpus


def BulkWorker(words: List[str], freqs: Dict[str, int], not_found_set: Set[str]):

    c = SessionBncCorpus()
    for word in words:
        f = c.get_frequency(word)
        if f is not None:
            freqs[word] = f
            print(word, f, file=sys.stderr, sep='\t')
        else:
            not_found_set.add(word)
