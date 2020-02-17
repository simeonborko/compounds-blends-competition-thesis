import re
from urllib.parse import urlencode
from urllib.request import urlopen
from time import sleep

import configuration as conf
from .AbstractCorpus import AbstractCorpus


class SlovakCorpusException(Exception):
    pass


def _get_page(query):
    """Download korpus page from savba.sk. Return string."""
    url = 'http://korpus.juls.savba.sk:8080/manatee.ks/do_query'
    params = {'query': query, 'corpname': 'prim-6.0-public-all'}
    response = urlopen(url + '?' + urlencode(params))
    body = response.read()
    return body.decode('utf-8')


def _extract(content) -> str:
    """Get count from page content."""
    pattern = '<div class="count">[0-9\.-]+/([0-9]+) \(([0-9]+)\)</div>'
    m = re.search(pattern, content)
    if m:
        return m.group(1)
    raise SlovakCorpusException('Count not found.')


def download_freq(word: str):
    if not word or not word.strip():
        return None
    word = word.strip()
    freq = None
    while freq is None:
        try:
            page = _get_page(word)
            freq = int(_extract(page))
        except SlovakCorpusException:
            if conf.DEBUG:
                print('Corpus try again')
            sleep(conf.CORPORA_SLOVAK_SLEEP_TIME_ERROR)

    if conf.DEBUG:
        print(word, freq, sep='\t')
    sleep(conf.CORPORA_SLOVAK_SLEEP_TIME_PREVENTIVE)

    return freq


class SlovakExactCorpus(AbstractCorpus):

    _TABLE_NAME = 'sk_exact'

    def _get_freq(self, word):
        return download_freq(word)


class SlovakSubstringCorpus(AbstractCorpus):

    _TABLE_NAME = 'sk_substring'

    def _get_freq(self, word):
        return download_freq(f'.*{word}.*')
