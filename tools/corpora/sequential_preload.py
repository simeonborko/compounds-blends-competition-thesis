from typing import Type, List
from .AbstractCorpus import AbstractCorpus


def sequential_preload(corpus_class: Type[AbstractCorpus], data: List[str]):
    with corpus_class(use_storage=True) as corp:
        loaded_keys = corp.storage.data_keys
        already_loaded_num = 0
        to_load_now: List[str] = []
        for word in data:
            if word in loaded_keys:
                already_loaded_num += 1
            else:
                to_load_now.append(word)

        print('Input words:', len(data), sep='\t')
        print('Already loaded:', already_loaded_num, sep='\t')
        print('To load now:', len(to_load_now), sep='\t')

        for i, word in enumerate(to_load_now, 1):
            freq = corp.get_frequency(word)
            print(i, word, freq, sep='\t')
