"""
Image - prefixes, sub_sub -> dom_half, dom_half_number
"""
from typing import Optional, Tuple

from yoyo import step

__depends__ = {}


# zmena nazvu: ALTER TABLE image CHANGE <OLD_NAME> <NEW_NAME> <COLUMN_DEFINITION>
# pridanie: ALTER TABLE image ADD <NAME> <COLUMN_DEFINITION> [ AFTER <AFTER_COLUMN> ]
# zrusenie: ALTER TABLE image DROP <NAME>


def prefix_step(old_name: str, definition: str, new_name: Optional[str] = None) -> Tuple[str, str]:
    # new name should be without prefix
    if new_name is None:
        new_name = old_name
    return (
        "ALTER TABLE image CHANGE {} im_{} {}".format(old_name, new_name, definition),
        "ALTER TABLE image CHANGE im_{} {} {}".format(new_name, old_name, definition),
    )


def add_step(name: str, definition: str, after: Optional[str] = None) -> Tuple[str, str]:
    return (
        "ALTER TABLE image ADD {} {} {}".format(
            name, definition,
            'AFTER {}'.format(after) if after else '',
        ),
        "ALTER TABLE image DROP {}".format(name),
    )


steps = [
    step(*prefix_step('sub_sem_cat', 'text')),
    step(*prefix_step('dom_sem_cat', 'text')),
    step(*add_step('im_shape_nonshape', 'text', 'im_dom_sem_cat')),
    step(*prefix_step('sub_name', 'text')),
    step(*prefix_step('dom_name', 'text')),
    step(*prefix_step('sub_number', 'int(11)')),
    step(*prefix_step('dom_number', 'int(11)')),
    step(*prefix_step('half_number', 'int(11)')),
    step(*prefix_step('sub_sub', 'text', new_name='dom_half')),
    step(*add_step('im_dom_half_number', 'int(11)'))
]
