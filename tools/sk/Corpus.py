import re
from urllib.parse import urlencode
from urllib.request import urlopen
from os.path import isfile
import json
from time import sleep


class Corpus:

    @staticmethod
    def __get_page(query):
        """Download korpus page from savba.sk. Return string."""
        url = 'http://korpus.juls.savba.sk:8080/manatee.ks/do_query'
        params = {'query': query, 'corpname': 'prim-6.0-public-all'}
        response = urlopen(url + '?' + urlencode(params))
        body = response.read()
        return body.decode('utf-8')

    @staticmethod
    def __extract(content):
        """Get count from page content."""
        pattern = '<div class="count">[0-9\.-]+/([0-9]+) \(([0-9]+)\)</div>'
        m = re.search(pattern, content)
        if m:
            return m.group(1)
        raise Exception('Count not found.')

    def get_frequency(self, word):

        if not word or not word.strip():
            return None

        if word in self.data:
            return self.data[word]

        freq = None
        while freq is None:
            try:
                page = self.__get_page(word)
                freq = int(self.__extract(page))
            except Exception:
                print('Corpus try again')
                sleep(30)

        self.data[word] = freq
        print(word, freq, sep='\t')
        sleep(5)

        return freq

    def __init__(self, filename: str):

        self.filename = filename

        if isfile(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)
