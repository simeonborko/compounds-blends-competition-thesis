import configuration
from tools import Connection
from tools.en.corpus.BasicBncCorpus import BasicBncCorpus
from tools.en.corpus.Preloader import Preloader

with Connection() as conn:
    q = 'SELECT DISTINCT sw_graphic FROM source_word WHERE survey_language = %s'
    c = conn.cursor()
    c.execute(q, ('EN',))

    all_words_set = {r[0] for r in c}

with BasicBncCorpus(configuration.BNC_CORPUS_FILE, configuration.BNC_CORPUS_NOT_FOUND_LIST_FILE) as corpus:

    word_list = list(all_words_set - corpus.data.keys() - corpus.not_found_set)

    print('Number of SW in DB:', len(all_words_set))
    print('Number of SW already loaded:', len(corpus.data))
    print('Number of SW not found in corpus:', len(corpus.not_found_set))
    print('Number of SW to load now:', len(word_list))

    res = Preloader(word_list)

    corpus.add_preloaded_data(*res)
