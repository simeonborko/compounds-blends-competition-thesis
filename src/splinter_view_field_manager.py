from collections import namedtuple
from itertools import chain
from typing import List, Tuple, Iterable, Dict, Set
from cached_property import cached_property

NameT = namedtuple('NameT', ('original', 'current'))


class SplinterViewFieldManager:

    naming_unit: List[NameT] = None
    image: List[NameT] = None
    source_word: Tuple[List[NameT], List[NameT], List[NameT], List[NameT]] = None
    splinter: Tuple[List[NameT], List[NameT], List[NameT], List[NameT]] = None
    spl_types: Tuple[str, ...] = None

    def __init__(self, nu_fields: Iterable[str], img_fields: Iterable[str], sw_fields: Iterable[str],
                 spl_fields: Iterable[str], spl_types: Tuple[str, ...]):
        self.naming_unit = [NameT(f, f) for f in nu_fields]
        self.image = [NameT(f, f) for f in img_fields]
        self.source_word = tuple(
            [
                NameT(f, self.__sw_original_to_current(f, i+1))
                for f in sw_fields
            ]
            for i in range(4)
        )
        self.splinter = tuple(
            [
                NameT(f, self.__spl_original_to_current(f, spl_type))
                for f in spl_fields
            ]
            for spl_type in spl_types
        )
        self.spl_types = spl_types

    @staticmethod
    def __sw_original_to_current(field: str, sw_number: int):
        if field.startswith('G_'):
            raise Exception('There should be no generated fields')
        if field.startswith('sw_'):
            field = field[3:]
        return 'sw{}_{}'.format(sw_number, field)

    @staticmethod
    def __spl_original_to_current(field: str, spl_type):
        if field == 'type_of_splinter':
            return '{}_name'.format(spl_type)
        gflag = field.startswith('G_')
        if gflag:
            field = field[2:]
        return ('G_{}_{}' if gflag else '{}_{}').format(spl_type, field)

    @cached_property
    def select_fields(self) -> List[str]:

        fields = []

        fields.extend('NU.' + n.original for n in self.naming_unit)

        fields.extend('I.' + n.original for n in self.image)

        for i, sw_names in enumerate(self.source_word):
            fields.extend('SW{}.{} {}'.format(i+1, n.original, n.current) for n in sw_names)

        for spl_type, spl_names in zip(self.spl_types, self.splinter):
            fields.extend('{}.{} {}'.format(spl_type.upper(), n.original, n.current) for n in spl_names)

        return fields

    @cached_property
    def flat_fields_naming_unit(self) -> List[str]:
        return [n.current for n in self.naming_unit]

    @cached_property
    def flat_fields_image(self) -> List[str]:
        return [n.current for n in self.image]

    @cached_property
    def flat_fields_source_word(self) -> List[str]:
        fields = []
        for sw_names in self.source_word:
            fields.extend(n.current for n in sw_names)
        return fields

    @cached_property
    def flat_fields_splinter(self) -> List[str]:
        fields = []
        for spl_names in self.splinter:
            fields.extend(n.current for n in spl_names)
        return fields

    @cached_property
    def flat_fields(self) -> List[str]:
        fields = []
        fields.extend(self.flat_fields_naming_unit)
        fields.extend(self.flat_fields_image)
        fields.extend(self.flat_fields_source_word)
        fields.extend(self.flat_fields_splinter)
        return fields

    @cached_property
    def static_fields(self) -> Set[str]:
        """Tieto stlpce sa nebudu editovat"""
        fields = set()
        fields.update(self.flat_fields_naming_unit)
        fields.update(self.flat_fields_image)
        fields.update(self.flat_fields_source_word)
        return fields

    @cached_property
    def current_to_original(self) -> Dict[str, str]:

        flat_names: List[NameT] = []
        flat_names.extend(self.naming_unit)
        flat_names.extend(self.image)
        flat_names.extend(chain.from_iterable(self.source_word))
        flat_names.extend(chain.from_iterable(self.splinter))

        return {n.current: n.original for n in flat_names}

    @cached_property
    def original_spl_to_current(self) -> Dict[str, Dict[str, str]]:
        """spl_type -> original -> current"""

        return {
            spl_type: {
                n.original: n.current
                for n in self.splinter[i]
            }
            for i, spl_type in enumerate(self.spl_types)
        }

