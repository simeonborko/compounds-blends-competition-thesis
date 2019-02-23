from tools.en.corpus.AbstractBncCorpus import AbstractBncCorpus
import requests


class SessionBncCorpus(AbstractBncCorpus):

    session = None

    def _get_page(self, query: str) -> str:
        if self.session is None:
            self.session = requests.Session()
        r = self.session.get(self.URL, params=self.params(query))
        return r.text


# c = SessionBncCorpus()
# print(c.get_frequency('duck'))
