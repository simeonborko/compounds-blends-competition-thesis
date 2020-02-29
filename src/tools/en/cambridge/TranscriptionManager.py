import sys
from typing import Optional
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from pyquery import PyQuery
from unidecode import unidecode

from src import configuration
from src.tools import CambridgeConnection
from src.tools.storage import DatabaseStorage


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
        query = query.lower()
        url = cls.URL + quote(query)
        response = urlopen(url)
        if url != response.url:
            # print('Request url {} nie je rovnaka ako response url {}'.format(url, response.url), file=sys.stderr)
            return None
        body = response.read().decode('utf-8')

        pq = PyQuery(body)

        entries = pq(".pr.entry-body__el")
        for entry in entries.items():
            # priklad: ak zadas billed, su tam dva zaznamy: billed, bill
            if entry.find('.headword .hw.dhw').text().lower() != query:
                continue
            ipa = entry.find('.ipa')
            if len(ipa) == 0:
                continue
            # 0 je UK, 1 je US
            return ipa.eq(0).text()

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
