from contextlib import contextmanager
from typing import Type

from .AbstractCorpus import AbstractCorpus


@contextmanager
def corpus_context_manager(corpus_class: Type[AbstractCorpus], entity_class, attrname: str):
    """
    :param corpus_class: trieda korpusu
    :param entity_class: trieda, ktorej chceme nastavit korpus
    :param attrname: nazov parametru triedy entity_class, kde sa ma ulozit korpus
    """
    with corpus_class() as corpus:
        setattr(entity_class, attrname, corpus)
        try:
            yield
        finally:
            setattr(entity_class, attrname, None)
