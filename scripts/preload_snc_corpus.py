from src.tools import Connection
from src.tools.corpora import SlovakExactCorpus, preload

def preload_sk(table, column):
    with Connection() as conn:
        q = 'SELECT DISTINCT {} FROM {} WHERE survey_language = %s'.format(column, table)
        c = conn.cursor()
        c.execute(q, ('SK',))

        all_words = [r[0] for r in c]

    preload(SlovakExactCorpus, all_words)

preload_sk('source_word', 'sw_graphic')
preload_sk('naming_unit', 'nu_graphic')
