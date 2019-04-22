import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, Set

from os.path import isfile

import sys

from requests.exceptions import ConnectionError

# /cgi-bin/json.pl?script=itcqp&curlang=en&c=BNC&registry=&q=%5Blemma=%22of%22%5D&cqpsyntaxonly=on&searchtype=conc&contextsize=0c&matchpos=middle&terminate=1&count=on&kellyLang=en&kelly=on&kellyFilterCount=0&kellyFilterLevel=1&callback=callback&_=1550933413665


class AbstractBncCorpus(ABC):
    URL = 'http://smlc12.leeds.ac.uk/cgi-bin/json.pl'

    PARAMS = {
        'script': 'itcqp',
        'curlang': 'en',
        'c': 'BNC',
        'registry': '',
        'cqpsyntaxonly': 'on',
        'searchtype': 'conc',
        'contextsize': '0c',
        'matchpos': 'middle',
        'terminate': '1',
        'count': 'on',
        'kellyLang': 'en',
        'kelly': 'on',
        'kellyFilterCount': '0',
        'kellyFilterLevel': '1',
        'callback': 'callback',
        '_': '1550933413665',
    }

    filename = None
    filename_not_found_list = None
    data = None
    not_found_set = None

    def params(self, query: str) -> Dict[str, str]:
        d = self.PARAMS.copy()
        d['q'] = '[lemma="{}"]'.format(query)
        return d

    @abstractmethod
    def _get_page(self, query: str) -> str:
        pass

    @staticmethod
    def _extract(content) -> Optional[int]:
        """
        Ziskat pocet z odpovede
        Priklad odpovede:
        callback([[{"cpos": "BNC.290033.290033", "titleid": "A0C", "left": "<span class=', UN ,'>,</span>", "match": "<span class='NN B1 duck'> duck</span>", "right": "<span class='NN B1 oven'> oven</span>", "stats": [0,0,0,2,0,0,1,3]}], {"count" : 1626}]);
        """
        try:
            # 9 je dlzka 'callback('
            # 2 je dlzka ');'
            content = content[9:-2]
            content = json.loads(content)

            if type(content) is list:
                return content[1]['count']

            if type(content) is dict and 'message' in content:
                print(content['message'], file=sys.stderr)

        except Exception as e:
            print(e, file=sys.stderr)

        return None

    def get_frequency(self, word: str) -> Optional[int]:

        word = word.strip()
        if not word:
            return None

        if self.data is not None and word in self.data:
            return self.data[word]

        if self.not_found_set is not None and word in self.not_found_set:
            return None

        attempts = 2
        page = None
        while page is None and attempts > 0:
            try:
                page = self._get_page(word)
            except ConnectionError as e:
                print('_get_page for "{}" failed'.format(word))
                attempts -= 1
                if attempts > 0:
                    print('Trying again...')

        freq = self._extract(page) if page is not None else None

        if freq is not None and self.data is not None:
            self.data[word] = freq

        if freq is None and self.not_found_set is not None:
            self.not_found_set.add(word)

        return freq

    def __init__(self, filename=None, filename_not_found_list=None):
        self.filename = filename
        self.filename_not_found_list = filename_not_found_list

    def __enter__(self):
        if isfile(self.filename):
            with open(self.filename, 'r') as fp:
                self.data = json.load(fp)
        else:
            self.data = {}

        if isfile(self.filename_not_found_list):
            with open(self.filename_not_found_list) as fp:
                self.not_found_set = set(json.load(fp))
        else:
            self.not_found_set = set()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.filename, 'w') as fp:
            json.dump(self.data, fp)
        with open(self.filename_not_found_list, 'w') as fp:
            json.dump(list(self.not_found_set), fp)

    def add_preloaded_data(self, preloaded: Dict[str, int], not_found: Set[str]):
        if self.data is not None and self.not_found_set is not None:
            self.data.update(preloaded)
            self.not_found_set.update(not_found)
        else:
            print('add_preloaded_data called outside of context manager (with)', file=sys.stderr)
