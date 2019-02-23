from tools.en.corpus.AbstractBncCorpus import AbstractBncCorpus
import requests


class BasicBncCorpus(AbstractBncCorpus):

    def _get_page(self, query: str) -> str:
        r = requests.get(self.URL, self.params(query))
        return r.text


# c = BasicBncCorpus()
# print(c.get_frequency('duck'))
