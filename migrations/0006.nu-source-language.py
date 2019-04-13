"""Pridat stlpec nu_source_language"""

from yoyo import step


steps = [
    step(
        "ALTER TABLE naming_unit ADD nu_source_language varchar(200) AFTER image_id",
        "ALTER TABLE naming_unit DROP nu_source_language",
    )
]
