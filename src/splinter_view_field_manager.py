from itertools import chain
from typing import List, Tuple, Iterable, Dict, Set, Union
from cached_property import cached_property

from src.tools import joined_column_sql


class Column:
    def __init__(self, sql_selector: Union[Tuple[str, str], str], alias_name: str):
        self.__sql_selector = sql_selector
        self.alias_name = alias_name

    def get_sql_column_name(self):
        if self.is_dynamic:
            raise ValueError("Cannot get sql column name for dynamically created column")
        return self.__sql_selector[1]

    @property
    def select_field(self):
        selector = '`{}`.`{}`'.format(*self.__sql_selector) if type(self.__sql_selector) is tuple else self.__sql_selector
        return f'{selector} AS {self.alias_name}'

    @property
    def is_dynamic(self):
        return type(self.__sql_selector) is not tuple


# class TableColumn(GeneralColumn):
#     def __init__(self, sql_table: str, column_name: str, alias_name: str):
#         super().__init__(f'`{sql_table}`.`{column_name}`', alias_name)
#         self.sql_table = sql_table
#         self.column_name = column_name


class SplinterViewFieldManager:
    naming_unit: List[Column] = None
    image: List[Column] = None
    source_word: Tuple[List[Column], ...] = None
    splinter: Tuple[List[Column], ...] = None
    spl_types: Tuple[str, ...] = None

    def __init__(self,
                 nu_fields: Iterable[str],
                 nu_joined_fields: Set[str],
                 img_fields: Iterable[str],
                 sw_fields: Iterable[str],
                 spl_fields: Iterable[str],
                 spl_types: Tuple[str, ...]):

        self.naming_unit = [
            Column(joined_column_sql(editable=f'NU.{field}', generated=f'NU.G_{field}'), field) if field in nu_joined_fields else Column(('NU', field), field)
            for field in nu_fields
        ]
        self.image = [Column(('I', f), f) for f in img_fields]
        self.source_word = tuple(
            [
                Column((f'SW{i+1}', f), self.__sw_original_to_current(f, i + 1))
                for f in sw_fields
            ]
            for i in range(4)
        )
        self.splinter = tuple(
            [
                Column((spl_type.upper(), f), self.__spl_original_to_current(f, spl_type))
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

        fields.extend(f.select_field for f in self.naming_unit)

        fields.extend(f.select_field for f in self.image)

        for sw_fields in self.source_word:
            fields.extend(f.select_field for f in sw_fields)

        for spl_fields in self.splinter:
            fields.extend(f.select_field for f in spl_fields)

        return fields

    @cached_property
    def flat_fields_naming_unit(self) -> List[str]:
        return [f.alias_name for f in self.naming_unit]

    @cached_property
    def flat_fields_image(self) -> List[str]:
        return [f.alias_name for f in self.image]

    @cached_property
    def flat_fields_source_word(self) -> List[str]:
        fields = []
        for sw_fields in self.source_word:
            fields.extend(f.alias_name for f in sw_fields)
        return fields

    @cached_property
    def flat_fields_splinter(self) -> List[str]:
        fields = []
        for spl_fields in self.splinter:
            fields.extend(f.alias_name for f in spl_fields)
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
        """Tieto stlpce sa nebudu editovat. Tato mnozina moze byt este upravena, tak pozri presne pouzitie."""
        fields = set()
        fields.update(self.flat_fields_naming_unit)
        fields.update(self.flat_fields_image)
        fields.update(self.flat_fields_source_word)
        return fields

    @cached_property
    def current_to_original(self) -> Dict[str, str]:
        """Excel names (aliasy) -> sql selektor"""

        general_columns: List[Column] = []
        general_columns.extend(self.naming_unit)
        general_columns.extend(self.image)
        general_columns.extend(chain.from_iterable(self.source_word))
        general_columns.extend(chain.from_iterable(self.splinter))

        return {f.alias_name: f.get_sql_column_name() for f in general_columns if f.is_dynamic}

    @cached_property
    def original_spl_to_current(self) -> Dict[str, Dict[str, str]]:
        """spl_type -> original (sql selektor) -> current (alias name)"""
        return {
            spl_type: {
                f.get_sql_column_name(): f.alias_name
                for f in self.splinter[i]
            }
            for i, spl_type in enumerate(self.spl_types)
        }
