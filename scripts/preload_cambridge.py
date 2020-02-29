from src.tools import Connection, sequential_preload_common
from src.tools.en import TranscriptionManager

with Connection() as conn:
    q = 'SELECT DISTINCT sw_graphic FROM source_word WHERE survey_language = %s'
    c = conn.cursor()
    c.execute(q, ('EN',))

    all_words = [r[0] for r in c]

with TranscriptionManager() as manager:
    sequential_preload_common(
        all_words,
        manager.storage,
        lambda word: manager[word]
    )
