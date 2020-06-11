"""Odstranit stlpce s priponou __ignore"""

from yoyo import step


def do_step(table, field):
    step(
        f"ALTER TABLE {table} DROP {field}",
        f"ALTER TABLE {table} ADD {field} tinyint(1)"
    )


nu_fields = [
    'G_nu_syllabic__ignore',
    'G_lexsh_main__ignore',
    'G_lexsh_sm__ignore',
    'G_lexsh_whatm__ignore',
]

sw_fields = [
    'G_sw_syllabic__ignore',
    'G_sw_phonetic__ignore',
]

for f in nu_fields:
    do_step("naming_unit", f)

for f in sw_fields:
    do_step('source_word', f)

for i in range(1, 4+1):
    do_step('splinter', f'G_sw{i}_splinter__ignore')
    do_step('splinter', f'G_sw{i}_splinter_len__ignore')
