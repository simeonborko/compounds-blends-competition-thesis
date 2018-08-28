from tools import Connection
from tools.sk import Corpus
import configuration

with Connection() as conn:
    c = conn.cursor()
    c.execute("SELECT sw_graphic FROM source_word WHERE survey_language = %s", ('SK',))
    with Corpus(configuration.CORPUS_FILE) as corpus:
        for word, in c:
            print(word, corpus.get_frequency(word))
