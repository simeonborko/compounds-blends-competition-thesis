"""Zmazat stlpec dom_half z NU, pretoze dom_half je v tabulke image"""

from yoyo import step

step(
    "ALTER TABLE naming_unit DROP dom_half",
    "ALTER TABLE naming_unit ADD dom_half varchar(200) AFTER what_connect_element"
)
