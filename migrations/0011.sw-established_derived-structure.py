"""Pridat stlpce established_derived, structure do source_word"""

from yoyo import step

step(
    "ALTER TABLE source_word ADD established_derived varchar(200) AFTER sw_word_class",
    "ALTER TABLE source_word DROP established_derived"
)

step(
    "ALTER TABLE source_word ADD structure varchar(200) AFTER sw_word_class",
    "ALTER TABLE source_word DROP structure"
)
