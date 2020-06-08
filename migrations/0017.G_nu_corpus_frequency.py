"""Premenovat nu_corpus_frequency na G_nu_corpus_frequency"""

from yoyo import step

step(
    "ALTER TABLE naming_unit CHANGE nu_corpus_frequency G_nu_corpus_frequency int(11)",
    "ALTER TABLE naming_unit CHANGE G_nu_corpus_frequency nu_corpus_frequency int(11)"
)
