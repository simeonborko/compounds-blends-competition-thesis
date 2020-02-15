from typing import Type, List

from tools import sequential_preload_common
from .AbstractCorpus import AbstractCorpus


def sequential_preload(corpus_class: Type[AbstractCorpus], data: List[str]):
    with corpus_class(use_storage=True) as corp:
        sequential_preload_common(
            data,
            corp.storage,
            lambda word: corp.get_frequency(word)
        )
