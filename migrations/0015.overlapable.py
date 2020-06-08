"""Pridat stlpce overlapable do naming_unit"""

from yoyo import step

after_column = 'nu_corpus_frequency'
new_columns = [
    ('G_overlapable', 'varchar(200)'),
    ('G_overlapable_length', 'int(11)'),
    ('G_overlapable_sw1', 'int(11)'),
    ('G_overlapable_sw2', 'int(11)')
]

for one_col in new_columns:
    step(
        f"ALTER TABLE naming_unit ADD {one_col[0]} {one_col[1]} AFTER {after_column}",
        f"ALTER TABLE naming_unit DROP {one_col[0]}"
    )
    after_column = one_col[0]
