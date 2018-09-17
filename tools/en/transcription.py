import json
from html.parser import HTMLParser
from typing import Optional
from urllib.request import urlopen

from os.path import isfile

from unidecode import unidecode

import configuration


class CambridgeParser(HTMLParser):

    inside = False
    found = False
    depth = 0
    text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            if len(attrs) == 1 and attrs[0][0] == 'class' and attrs[0][1] == 'ipa' and not self.found:
                self.inside = True
                self.found = True
            if self.inside:
                self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'span' and self.inside:
            self.depth -= 1
            if self.depth == 0:
                self.inside = False
            elif self.depth < 0:
                raise Exception

    def handle_data(self, data):
        if self.inside:
            self.text += data

    def error(self, message):
        raise NotImplementedError


class TranscriptionManager:
    URL = 'https://dictionary.cambridge.org/dictionary/english/'
    DATA_FILENAME = configuration.CAMBRIDGE_FILE

    def __init__(self):
        self.data = {}

    def __enter__(self):
        if isfile(self.DATA_FILENAME):
            with open(self.DATA_FILENAME) as fp:
                self.data = json.load(fp)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.DATA_FILENAME, 'w') as fp:
            json.dump(self.data, fp)

    @classmethod
    def download(cls, query: str) -> Optional[str]:
        """Stiahne z webu foneticky prepis query. Vracia foneticky prepis alebo None"""
        response = urlopen(cls.URL + query)
        body = response.read().decode('utf-8')

        parser = CambridgeParser()
        parser.feed(body)

        if len(parser.text) > 0:
            return parser.text
        else:
            return None

    def __getitem__(self, item: str) -> Optional[str]:

        # orezat a zmensit
        item = item.strip().lower()

        # ak ma diakritiku
        if unidecode(item) != item:
            return None

        if item not in self.data:
            self.data[item] = self.download(item)

        return self.data[item]
