from src.tools import Connection
from src.tools.corpora import EnglishExactCorpus, preload

def preload_en(table, column):
    with Connection() as conn:
        q = 'SELECT DISTINCT {} FROM {} WHERE survey_language = %s'.format(column, table)
        c = conn.cursor()
        c.execute(q, ('EN',))

        all_words = [r[0] for r in c]

    preload(EnglishExactCorpus, all_words)

preload_en('source_word', 'sw_graphic')
preload_en('naming_unit', 'nu_graphic')
