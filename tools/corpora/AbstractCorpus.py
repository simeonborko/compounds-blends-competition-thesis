from abc import ABC, abstractmethod
from typing import Optional

from tools.corpora import CorpStorage


class AbstractCorpus(ABC):

    _TABLE_NAME = None

    def __init__(self, use_storage: bool=True):

        if type(self._TABLE_NAME) is not str:
            raise Exception

        self._use_storage: bool = use_storage
        self._storage: Optional[CorpStorage] = None

    def __enter__(self):
        if self._use_storage:
            self._storage = CorpStorage(self._TABLE_NAME)
            self._storage.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._use_storage:
            self._storage.save()
            self._storage = None

    @abstractmethod
    def _get_freq(self, word) -> Optional[int]:
        pass

    def get_frequency(self, word) -> Optional[int]:
        if self._storage is not None and word in self._storage:
            return self._storage[word]
        freq = self._get_freq(word)
        if self._storage is not None:
            self._storage[word] = freq
        return freq

    @property
    def storage(self) -> Optional[CorpStorage]:
        return self._storage
