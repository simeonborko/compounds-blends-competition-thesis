"""Pridat stlpce nu_number_of_SWs, nu_OT, nu_TT do naming_unit"""

from yoyo import step

steps = [
    step(
        "ALTER TABLE naming_unit ADD nu_number_of_SWs varchar(200) AFTER nu_source_language",
        "ALTER TABLE naming_unit DROP nu_number_of_SWs",
    ),
    step(
        "ALTER TABLE naming_unit ADD nu_OT varchar(200) AFTER nu_number_of_SWs",
        "ALTER TABLE naming_unit DROP nu_OT",
    ),
    step(
        "ALTER TABLE naming_unit ADD nu_TT varchar(200) AFTER nu_OT",
        "ALTER TABLE naming_unit DROP nu_TT",
    ),
]
