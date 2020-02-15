import sys
from typing import Optional
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from unidecode import unidecode

import configuration
from tools import CambridgeConnection
from tools.storage import DatabaseStorage
from .CambridgeParser import CambridgeParser


class TranscriptionManager:
    URL = 'https://dictionary.cambridge.org/dictionary/english/'

    def __init__(self):
        self._storage: Optional[DatabaseStorage] = None

    def __enter__(self):
        self._storage = DatabaseStorage(
            'cambridge',
            'word', 'transcription',
            configuration.CAMBRIDGE_BACKUP_DIR,
            CambridgeConnection,
            "Error"
        )
        self._storage.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._storage.save()
        self._storage = None

    @classmethod
    def download(cls, query: str) -> Optional[str]:
        """Stiahne z webu foneticky prepis query. Vracia foneticky prepis alebo None"""
        url = cls.URL + quote(query.lower())
        response = urlopen(url)
        if url != response.url:
            print('Request url {} nie je rovnaka ako response url {}'.format(url, response.url), file=sys.stderr)
            return None
        body = response.read().decode('utf-8')

        parser = CambridgeParser()
        parser.feed(body)

        if len(parser.text) > 0:
            return parser.text
        else:
            return None

    def __getitem__(self, item: str) -> Optional[str]:

        item = item.strip()

        # ak ma diakritiku
        if unidecode(item) != item:
            return None

        if self._storage is not None and item in self._storage:
            return self._storage[item]
        try:
            transcription = self.download(item)
            if self._storage is not None:
                self._storage[item] = transcription
        except HTTPError as e:
            print('HTTPError while downloading from Cambridge for word', item, e, file=sys.stderr)
            self._storage.set_as_faulty(item)
            transcription = None

        return transcription

    @property
    def storage(self) -> Optional[DatabaseStorage]:
        return self._storage
