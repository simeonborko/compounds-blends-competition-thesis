from io import StringIO
from typing import Optional

import requests
from lxml import etree

from .AbstractCorpus import AbstractCorpus


_PARAMS = {
    'type': 'simple',
    'mode': 'PHRASE',
    'index': 'exact',
    'sortby': 'random',
    'matches': '10',
    'powerselect': ''
}


def _get_page(query):
    params = {
        **_PARAMS,
        'query': query,
        'queries': query,
    }
    r = requests.post('http://phrasesinenglish.org/searchBNC.php', data=params)
    return r.text


def _extract(content) -> Optional[str]:
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(content), parser)
    root = tree.getroot()
    tbl = root.find('body').find('table')
    if tbl is None:
        return None
    cell = tbl[2][1]
    return cell.text.replace(',', '')


def download_freq(word: str):
    if not word or not word.strip():
        return None
    word = word.strip()
    page = _get_page(word)
    freq = _extract(page)
    if freq is not None:
        return int(freq)
    else:
        return None


class EnglishExactCorpus(AbstractCorpus):

    _TABLE_NAME = 'en_exact'

    def _get_freq(self, word):
        return download_freq(word)


class EnglishSubstringCorpus(AbstractCorpus):

    _TABLE_NAME = 'en_substring'

    def _get_freq(self, word):
        return download_freq(f'*{word}*')

