from abc import ABC, abstractmethod
from typing import Optional

import sys
import http.client

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
        """
        Ziskaj frekvenciu pre zadany vyraz.
        :param word: vyraz na vyhladanie v korpuse
        :return: frekvencia (int), alebo 0 ak sa vyraz nenasiel, alebo None v pripade chyby
        """
        if self._storage is not None and word in self._storage:
            freq = self._storage[word]
            return freq if freq is not None else 0
        try:
            freq = self._get_freq(word)
            if freq is None:
                freq = 0
            if self._storage is not None:
                self._storage[word] = freq
        except http.client.RemoteDisconnected as e:
            if self._storage is not None:
                self._storage.set_as_faulty(word)
            print(word, e, file=sys.stderr)
            freq = None
        except http.client.HTTPException as e:
            print(word, e, file=sys.stderr)
            freq = None

        return freq

    @property
    def storage(self) -> Optional[CorpStorage]:
        return self._storage
