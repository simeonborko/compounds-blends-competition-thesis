import configuration as conf
from tools import Connection
from tools.sk import Corpus

with Connection() as conn:
    q = 'SELECT DISTINCT sw_graphic FROM source_word WHERE survey_language = %s'
    c = conn.cursor()
    c.execute(q, ('SK',))

    all_words = [r[0] for r in c]

with Corpus(conf.CORPUS_FILE) as corp:
    for word in all_words:
        print(word, corp.get_frequency(word))
