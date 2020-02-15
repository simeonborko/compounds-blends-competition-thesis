import http.client
import sys
from abc import ABC, abstractmethod
from typing import Optional

import configuration
from tools import CorpConnection
from tools.storage import DatabaseStorage


class AbstractCorpus(ABC):

    _TABLE_NAME = None

    def __init__(self, use_storage: bool = True):

        if type(self._TABLE_NAME) is not str:
            raise Exception

        self._use_storage: bool = use_storage
        self._storage: Optional[DatabaseStorage] = None

    def __enter__(self):
        if self._use_storage:
            self._storage = DatabaseStorage(
                self._TABLE_NAME,
                'word', 'freq',
                configuration.CORPORA_BACKUP_DIR,
                CorpConnection,
                -1
            )
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
    def storage(self) -> Optional[DatabaseStorage]:
        return self._storage
