"""
NamingUnit - pridanie stlpcekov what_connect_element, dom_half
"""

from yoyo import step


steps = [
    step(
        "ALTER TABLE naming_unit ADD what_connect_element varchar(200) AFTER connect_element",
        "ALTER TABLE naming_unit DROP what_connect_element"
    ),
    step(
        "ALTER TABLE naming_unit ADD dom_half varchar(200) AFTER what_connect_element",
        "ALTER TABLE naming_unit DROP dom_half"
    )
]