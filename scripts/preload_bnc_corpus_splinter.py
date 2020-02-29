import itertools

from src.tools import Connection
from src.tools.corpora import EnglishExactCorpus, EnglishSubstringCorpus, preload

query = """SELECT
  IF(S.sw1_splinter IS NULL OR S.sw1_splinter = '', S.G_sw1_splinter, S.sw1_splinter) AS splinter_1,
  IF(S.sw2_splinter IS NULL OR S.sw2_splinter = '', S.G_sw2_splinter, S.sw2_splinter) AS splinter_2,
  IF(S.sw3_splinter IS NULL OR S.sw3_splinter = '', S.G_sw3_splinter, S.sw3_splinter) AS splinter_3,
  IF(S.sw4_splinter IS NULL OR S.sw4_splinter = '', S.G_sw4_splinter, S.sw4_splinter) AS splinter_4
FROM splinter S
  LEFT JOIN naming_unit NU
    ON NU.nu_graphic=S.nu_graphic AND NU.first_language=S.first_language AND
       NU.survey_language=S.survey_language AND NU.image_id=S.image_id
WHERE
  S.survey_language = 'EN'
  AND NU.wf_process = 'blend'
  AND type_of_splinter LIKE 'graphic %';"""

with Connection() as conn:
    c = conn.cursor()
    c.execute(query)

    all_words = list(set(filter(lambda x: x is not None, itertools.chain.from_iterable(c))))

preload(EnglishExactCorpus, all_words)
preload(EnglishSubstringCorpus, all_words)
