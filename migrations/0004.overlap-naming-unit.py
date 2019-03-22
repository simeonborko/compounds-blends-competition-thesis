"""
Pridat [G_]overlapping_letters, [G_]overlapping_phones do naming unit tabulky.
"""

from yoyo import step


def build_args(name, after):
    return (
        "ALTER TABLE naming_unit ADD {} varchar(200) AFTER {}".format(name, after),
        "ALTER TABLE naming_unit DROP {}".format(name)
    )


steps = [
    step(*build_args("overlapping_letters", "nu_syllabic_len")),
    step(*build_args("overlapping_phones", "overlapping_letters")),
    step(*build_args("G_overlapping_letters", "G_nu_syllabic_len")),
    step(*build_args("G_overlapping_phones", "G_overlapping_letters")),
]
