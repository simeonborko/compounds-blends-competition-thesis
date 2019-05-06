from tools import Connection
from tools.corpora import SlovakExactCorpus, preload

with Connection() as conn:
    q = 'SELECT DISTINCT sw_graphic FROM source_word WHERE survey_language = %s'
    c = conn.cursor()
    c.execute(q, ('SK',))

    all_words = [r[0] for r in c]

preload(SlovakExactCorpus, all_words)
