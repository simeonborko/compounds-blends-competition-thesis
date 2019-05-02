from contextlib import contextmanager
from typing import Type

from .AbstractCorpus import AbstractCorpus

@contextmanager
def corpus_context_manager(corpus_class: Type[AbstractCorpus], before_fn, after_fn):
    """
    :param corpus_class: trieda korpusu
    :param before_fn: jednoparametrova funkcia, kde parameter je instancia korpusu a zavola sa na zaciatku
    :param after_fn: bezparametrova funkcia, ktora sa zavola na konci vo finally klauzule
    """
    with corpus_class() as corpus:
        before_fn(corpus)
        try:
            yield
        finally:
            after_fn()
