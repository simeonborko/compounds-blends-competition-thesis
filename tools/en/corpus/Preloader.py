from typing import List, Dict, Set
from tools.en.corpus.BulkWorker import BulkWorker
from threading import Thread

SIZE = 15


def Preloader(words: List[str]) -> (Dict[str, int], Set[str]):

    threads: List[Thread] = []
    freq_dicts: List[Dict[str, int]] = []
    not_found_sets: List[Set[str]] = []

    for i in range(SIZE):
        bulk = words[i::SIZE]

        freqs = {}
        not_found = set()
        t = Thread(target=BulkWorker, args=(bulk, freqs, not_found))
        t.start()

        freq_dicts.append(freqs)
        not_found_sets.append(not_found)
        threads.append(t)

    dct: Dict[str, int] = {}
    st: Set[str] = set()

    for thread, freqs, not_found in zip(threads, freq_dicts, not_found_sets):
        thread.join()
        dct.update(freqs)
        st.update(not_found)

    return dct, st
