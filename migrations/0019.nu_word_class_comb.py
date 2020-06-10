"""Premenovat nu_word_class na nu_word_class_comb"""

from yoyo import step

step(
    "ALTER TABLE naming_unit CHANGE nu_word_class nu_word_class_comb varchar(200)",
    "ALTER TABLE naming_unit CHANGE nu_word_class_comb nu_word_class varchar(200)"
)
