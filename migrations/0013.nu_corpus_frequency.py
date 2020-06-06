"""Pridat stlpec nu_corpus_frequency do naming_unit"""

from yoyo import step

step(
    "ALTER TABLE naming_unit ADD nu_corpus_frequency int(11) AFTER G_split_point_3",
    "ALTER TABLE naming_unit DROP nu_corpus_frequency"
)
