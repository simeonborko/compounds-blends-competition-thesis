"""Virtualne stlpce spajajuce upravovatelne a generovane stlpce"""

from yoyo import step


def do_step(table, field):
    data_type = "int(11)" if field.startswith('n_of_') or field.endswith('_len') else 'varchar(200)'
    step(
        f"ALTER TABLE {table} ADD J_{field} {data_type} AS (IF({field} IS NOT NULL AND {field} != '' OR G_{field} = 'NA', {field}, G_{field}))",
        f"ALTER TABLE {table} DROP J_{field}"
    )


nu_fields = [
    'nu_syllabic',
    'nu_graphic_len',
    'nu_phonetic_len',
    'nu_syllabic_len',
    'overlapping_letters',
    'overlapping_phones',
    'n_of_overlapping_letters',
    'n_of_overlapping_phones',
    'lexsh_main',
    'lexsh_sm',
    'lexsh_whatm',
    'split_point_1',
    'split_point_2',
    'split_point_3',
]

sw_fields = [
    'sw_phonetic',
    'sw_syllabic',
    'sw_graphic_len',
    'sw_phonetic_len',
    'sw_syllabic_len',
]

for f in nu_fields:
    do_step("naming_unit", f)

for f in sw_fields:
    do_step('source_word', f)

for i in range(1, 4+1):
    do_step('splinter', f'sw{i}_splinter')
    do_step('splinter', f'sw{i}_splinter_len')
