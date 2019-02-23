from urllib.parse import urlencode
from urllib.request import urlopen
from tools.en.corpus.AbstractBncCorpus import AbstractBncCorpus


class UrlLibBncCorpus(AbstractBncCorpus):

    def _get_page(self, query: str) -> str:
        """
        Example GET request:
        /cgi-bin/json.pl?script=itcqp&curlang=en&c=BNC&registry=&q=%5Blemma=%22duck%22%5D&cqpsyntaxonly=on&searchtype=conc&contextsize=0c&matchpos=middle&terminate=1&count=on&kellyLang=en&kelly=on&kellyFilterCount=0&kellyFilterLevel=1&callback=callback&_=1550933413665
        """
        url = self.URL + '?' + urlencode(self.params(query))
        # print(url)
        response = urlopen(url)
        body = response.read()
        return body.decode('utf-8')


# bnc = UrlLibBncCorpus()
# print(bnc.get_frequency('crocodile'))
# print(bnc.get_frequency('duck'))
# print(bnc.get_frequency('giraffe'))
