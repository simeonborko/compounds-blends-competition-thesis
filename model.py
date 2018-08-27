from abc import ABC, ABCMeta, abstractmethod
import sys
from collections import namedtuple
from typing import Iterable, Tuple

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from pymysql.cursors import DictCursor
import configuration
from entity import SourceWord, NamingUnit, Splinter
from tools import sk


class TableLike(ABC):

    _NAME = None
    _FIELDS = None
    _PRIMARY = None  # pocet stlpcov zo zaciatku
    _EXPORT_SELECT = None

    _REDFILL = PatternFill("solid", fgColor="FF7575")
    _YELLOWFILL = PatternFill("solid", fgColor="FFFC75")
    _NOFILL = PatternFill()

    ExecuteResult = namedtuple('ExecuteResult', ['cursor', 'result'])

    def __init__(self, wb: Workbook, conn):
        self._wb = wb
        self.__conn = conn

    def _add_header(self, sheet):
        sheet.append(self._FIELDS)
        emphasized = set(self._emphasized_columns)
        for i in range(len(self._FIELDS)):
            sheet.cell(row=1, column=i + 1).font = Font(italic=True) if i in emphasized else Font(bold=True)

    @property
    def _emphasized_columns(self) -> Iterable[int]:
        """Vrati indexy zvyraznenych stlpcov (ktore nemaju byt upravovane)."""
        return range(self._PRIMARY)

    def _execute(self, *args, **kwargs) -> ExecuteResult:
        c = self.__conn.cursor(**kwargs)
        res = c.execute(*args) or 0
        return self.ExecuteResult(c, res)

    def _executemany(self, *args, **kwargs) -> ExecuteResult:
        c = self.__conn.cursor(**kwargs)
        res = c.executemany(*args) or 0
        return self.ExecuteResult(c, res)

    @abstractmethod
    def _sync(self, vals_gen) -> bool:
        """
        Synchronizuje dane riadky.
        :param vals_gen: generator na dvojice (zoznam hodnot v DB, zoznam Cell v SHEETE)
        """
        pass

    def create_sheet(self) -> bool:
        if self.sheet_created:
            return False

        sheet = self._wb.create_sheet(self._NAME)

        # nadpisy
        self._add_header(sheet)

        # data
        for row in self._execute(self._EXPORT_SELECT).cursor:
            sheet.append(row)

        return True

    def sync(self, unhighlight: bool = False) -> bool:
        # ziskat zaznamy z DB
        db_dict = {dbvals[:self._PRIMARY]: list(dbvals) for dbvals in self._execute(self._EXPORT_SELECT).cursor}

        # ziskat zaznamy zo SHEETU
        sheet = self._wb[self._NAME]
        sheet_dict = {
            tuple(cell.value for cell in rows[:self._PRIMARY]): rows
            for rows in sheet.iter_rows(min_row=2)
        }

        # porovnat mnoziny klucov
        keys_db_only = db_dict.keys() - sheet_dict.keys()
        keys_sheet_only = sheet_dict.keys() - db_dict.keys()
        keys_both = db_dict.keys() & sheet_dict.keys()

        # odstranit predosle zvyraznenie
        if unhighlight:
            for row in sheet_dict.values():
                for cell in row:
                    if cell.fill == self._YELLOWFILL:
                        cell.fill = self._NOFILL

        modified = False

        # co su iba v DB, pridat zlto
        if len(keys_db_only) > 0:
            modified = True
            starting_row = sheet.max_row + 1
            for key in keys_db_only:
                sheet.append(db_dict[key])
            for row in sheet.iter_rows(min_row=starting_row):
                for cell in row:
                    cell.fill = self._YELLOWFILL

        # co su iba v SHEET, ofarbit cerveno
        if len(keys_sheet_only) > 0:
            for key in keys_sheet_only:
                for cell in sheet_dict[key]:
                    if cell.fill != self._REDFILL:
                        cell.fill = self._REDFILL
                        modified = True

        # co su aj aj, synchronizovat, zafarbit zlto zmenene
        return self._sync((db_dict[k], sheet_dict[k]) for k in keys_both) or modified

    @property
    def primary_fields(self) -> tuple: return self._FIELDS[:self._PRIMARY]

    @classmethod
    def name(cls) -> str: return cls._NAME

    @property
    def fields(self) -> tuple: return self._FIELDS

    @property
    def sheet_created(self) -> bool: return self._NAME in self._wb.sheetnames


class StaticView(TableLike):

    @property
    def _emphasized_columns(self) -> Iterable[int]:
        return range(len(self._FIELDS))

    def _sync(self, vals_gen):
        """Nahradi hodnoty v SHEETE hodnotami z DB"""
        modified = False
        for db_values, sheet_cells in vals_gen:
            for value, cell in zip(db_values, sheet_cells):
                if cell.value != value and (cell.value is not None or value != ''):
                    modified = True
                    cell.value = value
                    cell.fill = self._YELLOWFILL
        return modified


class Overview(StaticView):

    _NAME = 'overview'
    _FIELDS = (
        'respondent_id',
        'image_id',
        'nu_graphic',
        'age',
        'sex',
        'first_language',
        'survey_language',
        'sub_sem_cat',
        'dom_sem_cat',
        'sub_name',
        'dom_name',
        'sub_number',
        'dom_number',
        'half_number',
        'nu_phonetic',
        'nu_syllabic',
        'nu_graphic_len',
        'nu_phonetic_len',
        'nu_syllabic_len',
        'sw1_graphic',
        'sw2_graphic',
        'sw3_graphic',
        'sw4_graphic',
        'sw1_word_class',
        'sw2_word_class',
        'sw3_word_class',
        'sw4_word_class',
        'sw1_source_language',
        'sw2_source_language',
        'sw3_source_language',
        'sw4_source_language',
        'sw1_graphic_len',
        'sw2_graphic_len',
        'sw3_graphic_len',
        'sw4_graphic_len',
        'sw1_phonetic',
        'sw2_phonetic',
        'sw3_phonetic',
        'sw4_phonetic',
        'sw1_phonetic_len',
        'sw2_phonetic_len',
        'sw3_phonetic_len',
        'sw4_phonetic_len',
        'sw1_syllabic',
        'sw2_syllabic',
        'sw3_syllabic',
        'sw4_syllabic',
        'sw1_syllabic_len',
        'sw2_syllabic_len',
        'sw3_syllabic_len',
        'sw4_syllabic_len',
        'sw1_frequency_in_snc',
        'sw2_frequency_in_snc',
        'sw3_frequency_in_snc',
        'sw4_frequency_in_snc',
        'gs_name',
        'gs_sw1_splinter',
        'gs_sw2_splinter',
        'gs_sw3_splinter',
        'gs_sw4_splinter',
        'gs_sw1_splinter_len',
        'gs_sw2_splinter_len',
        'gs_sw3_splinter_len',
        'gs_sw4_splinter_len',
        'gs_sw1_splinter_len_to_sw_len',
        'gs_sw2_splinter_len_to_sw_len',
        'gs_sw3_splinter_len_to_sw_len',
        'gs_sw4_splinter_len_to_sw_len',
        'gs_sw1_splinter_len_to_nu_len',
        'gs_sw2_splinter_len_to_nu_len',
        'gs_sw3_splinter_len_to_nu_len',
        'gs_sw4_splinter_len_to_nu_len',
        'gm_name',
        'gm_sw1_splinter',
        'gm_sw2_splinter',
        'gm_sw3_splinter',
        'gm_sw4_splinter',
        'gm_sw1_splinter_len',
        'gm_sw2_splinter_len',
        'gm_sw3_splinter_len',
        'gm_sw4_splinter_len',
        'gm_sw1_splinter_len_to_sw_len',
        'gm_sw2_splinter_len_to_sw_len',
        'gm_sw3_splinter_len_to_sw_len',
        'gm_sw4_splinter_len_to_sw_len',
        'gm_sw1_splinter_len_to_nu_len',
        'gm_sw2_splinter_len_to_nu_len',
        'gm_sw3_splinter_len_to_nu_len',
        'gm_sw4_splinter_len_to_nu_len',
        'ps_name',
        'ps_sw1_splinter',
        'ps_sw2_splinter',
        'ps_sw3_splinter',
        'ps_sw4_splinter',
        'ps_sw1_splinter_len',
        'ps_sw2_splinter_len',
        'ps_sw3_splinter_len',
        'ps_sw4_splinter_len',
        'ps_sw1_splinter_len_to_sw_len',
        'ps_sw2_splinter_len_to_sw_len',
        'ps_sw3_splinter_len_to_sw_len',
        'ps_sw4_splinter_len_to_sw_len',
        'ps_sw1_splinter_len_to_nu_len',
        'ps_sw2_splinter_len_to_nu_len',
        'ps_sw3_splinter_len_to_nu_len',
        'ps_sw4_splinter_len_to_nu_len',
        'pm_name',
        'pm_sw1_splinter',
        'pm_sw2_splinter',
        'pm_sw3_splinter',
        'pm_sw4_splinter',
        'pm_sw1_splinter_len',
        'pm_sw2_splinter_len',
        'pm_sw3_splinter_len',
        'pm_sw4_splinter_len',
        'pm_sw1_splinter_len_to_sw_len',
        'pm_sw2_splinter_len_to_sw_len',
        'pm_sw3_splinter_len_to_sw_len',
        'pm_sw4_splinter_len_to_sw_len',
        'pm_sw1_splinter_len_to_nu_len',
        'pm_sw2_splinter_len_to_nu_len',
        'pm_sw3_splinter_len_to_nu_len',
        'pm_sw4_splinter_len_to_nu_len',
    )
    _EXPORT_SELECT = 'SELECT {} FROM overview'.format(
        ', '.join(_FIELDS)
    )

    _PRIMARY = 3


class EditableTableLike(TableLike):

    _EXCLUDE_EDITABLE = None
    _INCLUDE_EDITABLE = None

    def __init__(self, wb: Workbook, conn):
        super().__init__(wb, conn)
        self.__editable, self.__generated = self.__split_fields()

    @staticmethod
    def __looks_like_generated(field) -> bool:
        return field[:2] == 'G_' and field[-8:] != '__ignore'

    def __is_generated(self, field):
        if self._EXCLUDE_EDITABLE and field in self._EXCLUDE_EDITABLE:
            return True
        elif self._INCLUDE_EDITABLE and field in self._INCLUDE_EDITABLE:
            return False
        else:
            return self.__looks_like_generated(field)

    def __split_fields(self) -> (Tuple[int], Tuple[int]):
        editable = []
        generated = []
        for i, field in enumerate(self._FIELDS[self._PRIMARY:], self._PRIMARY):
            (generated if self.__is_generated(field) else editable).append(i)
        return tuple(editable), tuple(generated)

    @property
    def _emphasized_columns(self) -> Iterable[int]:
        return set(super()._emphasized_columns) | set(self.__generated)

    def _sync(self, vals_gen):
        whole_modif = False

        for db_values, sheet_cells in vals_gen:

            modified = False
            for i in self.__editable:
                if db_values[i] != sheet_cells[i].value and (db_values[i] or sheet_cells[i].value):
                    db_values[i] = sheet_cells[i].value
                    modified = True
                    whole_modif = True
            if modified:
                self._update(db_values)

            for i in self.__generated:
                if db_values[i] != sheet_cells[i].value and (db_values[i] or sheet_cells[i].value):
                    sheet_cells[i].value = db_values[i]
                    sheet_cells[i].fill = self._YELLOWFILL
                    whole_modif = True

        return whole_modif

    @abstractmethod
    def _update(self, datarow):
        """Aktualizuje data v DB podla `datarow`.
        Neoveruje, ci sa nezmenili hodnoty v needitovatelnych stlpcoch; to musi zariadit volajuci."""
        pass

    @property
    def generated_fields(self) -> tuple:
        return tuple(self._FIELDS[i] for i in self.__generated)

    @property
    def editable_fields(self) -> tuple:
        return tuple(self._FIELDS[i] for i in self.__editable)


class Table(EditableTableLike, metaclass=ABCMeta):

    # select iba na tie riadky, ktore potrebuju byt generovane
    _GENERATE_SELECT_NEEDED = None

    # select na vsetky riadky pri generovani (napr. Splinter potrebuje aj udaje zo SourceWord)
    _GENERATE_SELECT_ALL = None

    # select na riadky, ake primarne kluce maju byt v danej tabulke
    _INTEGRITY_SELECT = None

    def __init__(self, wb: Workbook, conn, fields=None):
        super().__init__(wb, conn)
        self._EXPORT_SELECT = "SELECT {} FROM {}".format(','.join(self._FIELDS), self._NAME)
        if self._GENERATE_SELECT_ALL is None:  # SplinterTable ma _GENERATE_SELECT_ALL v triede, nie v inite
            self._GENERATE_SELECT_ALL = "SELECT * FROM {}".format(self._NAME)  # treba *, nestaci self._FIELDS
        self.__field_mask = self.__create_field_mask(fields)

    def __create_field_mask(self, fields) -> tuple:
        """
        Maska poli je n-tica indexov do _FIELDS.
        Primarne polia zostanu vzdy zachovane.
        :param fields nazvy poli, ktore sa maju zachovat; alebo None
        :return maska poli
        """
        if fields is None:
            return tuple(range(len(self._FIELDS)))

        if tuple(fields[:self._PRIMARY]) != self.primary_fields:
            raise Exception

        fset = set(fields)
        return tuple(idx for idx, field in enumerate(self._FIELDS) if field in fset)

    def _update(self, datarow):
        if len(datarow) != len(self.__field_mask):
            raise Exception
        query = "UPDATE {} SET {} WHERE {}".format(
            self._NAME,
            ', '.join(self._FIELDS[i] + " = %s" for i in self.__field_mask[self._PRIMARY:]),
            ' AND '.join(f + " = %s" for f in self.primary_fields)
        )
        data = datarow[self._PRIMARY:] + datarow[:self._PRIMARY]
        self._execute(query, data)

    def _generate(self, force: bool, cls) -> int:

        c = self._execute(
            self._GENERATE_SELECT_ALL if force or not self._GENERATE_SELECT_NEEDED else self._GENERATE_SELECT_NEEDED,
            cursor=DictCursor
        ).cursor

        args = []

        for data in c:
            entity = cls(self, data)
            entity.generate()
            if entity.modified:
                args.append(entity.data)

        if len(args):

            query = "UPDATE {} SET {} WHERE {}".format(
                self._NAME,
                ", ".join("{0}=%({0})s".format(g) for g in self.generated_fields),
                " AND ".join("{0}=%({0})s".format(p) for p in self.primary_fields)
            )

            affected = self._executemany(query, args).result

            if len(args) != affected:
                print("Pocet args: {}, pocet affected: {}".format(len(args), affected), file=sys.stderr)
                affected = affected or 0

            return affected

        else:
            return 0

    def integrity_add(self) -> int:
        return self._execute(
            "INSERT IGNORE INTO {} ({}) {}".format(
                self._NAME,
                ', '.join(self.primary_fields),
                self._INTEGRITY_SELECT
            )
        ).result

    def integrity_junk(self) -> int:
        exres = self._execute(
            "SELECT {} FROM {} TBL LEFT JOIN ({}) TMP ON {} WHERE {}".format(
                ', '.join('TBL.' + field for field in self._FIELDS),
                self._NAME,
                self._INTEGRITY_SELECT,
                ' AND '.join('TBL.{0} = TMP.{0}'.format(p) for p in self.primary_fields),
                ' AND '.join('TMP.{} IS NULL'.format(p) for p in self.primary_fields)
            )
        )
        if not exres.result:
            return 0

        # vytvorit harok
        sheetname = 'junk {}'.format(self._NAME)
        if sheetname not in self._wb.sheetnames:
            sheet = self._wb.create_sheet(sheetname)
            self._add_header(sheet)
        else:
            sheet = self._wb[sheetname]

        # pridat riadky a ulozit kluce
        keys = []
        for row in exres.cursor:
            keys.append(row[:self._PRIMARY])
            sheet.append(row)

        exres = self._executemany(
            """DELETE FROM {} WHERE {}""".format(
                self._NAME,
                ' AND '.join('{} = %s'.format(p) for p in self.primary_fields)
            ),
            keys
        )
        return exres.result


class ImageTable(Table):
    _NAME = 'image'
    _FIELDS = (
        'image_id', 'sub_sem_cat', 'dom_sem_cat', 'sub_name', 'dom_name',
        'sub_number', 'dom_number', 'half_number', 'sub_sub'
    )
    _PRIMARY = 1


class LanguageTable(Table):
    _NAME = 'language'
    _FIELDS = ('code', 'name')
    _PRIMARY = 1
    _INTEGRITY_SELECT = "SELECT first_language code FROM respondent UNION SELECT survey_language code FROM respondent"


class NamingUnitTable(Table):
    _NAME = 'naming_unit'
    _FIELDS = (
        'nu_graphic', 'first_language', 'survey_language', 'image_id',
        'wf_process',

        'sw1_graphic', 'sw2_graphic', 'sw3_graphic', 'sw4_graphic',
        'sw1_headmod', 'sw2_headmod', 'sw3_headmod', 'sw4_headmod',
        'sw1_subdom', 'sw2_subdom', 'sw3_subdom', 'sw4_subdom',

        'nu_word_class', 'nu_phonetic',
        'nu_syllabic', 'G_nu_syllabic', 'G_nu_syllabic__ignore',
        'nu_graphic_len', 'G_nu_graphic_len',
        'nu_phonetic_len', 'G_nu_phonetic_len',
        'nu_syllabic_len', 'G_nu_syllabic_len',
        'n_of_overlapping_letters', 'G_n_of_overlapping_letters',
        'n_of_overlapping_phones', 'G_n_of_overlapping_phones',
        'lexsh_main', 'G_lexsh_main', 'G_lexsh_main__ignore', 'lexsh_sm', 'G_lexsh_sm', 'G_lexsh_sm__ignore',
        'lexsh_whatm', 'G_lexsh_whatm', 'G_lexsh_whatm__ignore',
        'split_point_1', 'G_split_point_1', 'split_point_2', 'G_split_point_2', 'split_point_3', 'G_split_point_3'
    )
    _PRIMARY = 4

    _GENERATE_SELECT_NEEDED = """select * from {} where
  survey_language='SK' and G_nu_syllabic is null
  or G_nu_graphic_len is null
  or nu_phonetic is not null and G_nu_phonetic_len is null
  or survey_language='SK' and G_nu_syllabic_len is null
  or survey_language='EN' and nu_phonetic is not null and G_nu_syllabic_len is null""".format(_NAME)

    _INTEGRITY_SELECT = "SELECT DISTINCT {} FROM response NATURAL JOIN respondent".format(', '.join(_FIELDS[:_PRIMARY]))

    def generate(self, force, **kwargs) -> int:
        return self._generate(force, NamingUnit)


class RespondentTable(Table):
    _NAME = 'respondent'
    _FIELDS = (
        'respondent_id', 'first_language', 'survey_language', 'first_language_original', 'second_language',
        'other_language', 'age', 'sex', 'sex_original', 'employment', 'education', 'birth_place', 'year_of_birth',
        'responding_date'
    )
    _PRIMARY = 1


class ResponseTable(Table):
    _NAME = 'response'
    _FIELDS = ('respondent_id', 'image_id', 'nu_graphic')
    _PRIMARY = 3


class SourceWordTable(Table):
    _NAME = 'source_word'
    _FIELDS = ('sw_graphic', 'first_language', 'survey_language',
               'source_language', 'sw_phonetic', 'sw_word_class',
               'sw_syllabic', 'G_sw_syllabic', 'G_sw_syllabic__ignore',
               'sw_graphic_len', 'G_sw_graphic_len',
               'sw_phonetic_len', 'G_sw_phonetic_len',
               'sw_syllabic_len', 'G_sw_syllabic_len', 'frequency_in_snc')
    _PRIMARY = 3
    _EXCLUDE_EDITABLE = {'frequency_in_snc'}
    _GENERATE_SELECT_NEEDED = """select * from {} where
  survey_language='SK' and G_sw_syllabic is null
  or G_sw_graphic_len is null
  or sw_phonetic is not null and G_sw_phonetic_len is null
  or survey_language='SK' and G_sw_syllabic_len is null
  or survey_language='EN' and sw_phonetic is not null and G_sw_syllabic_len is null
  or survey_language='SK' and frequency_in_snc is null""".format(_NAME)

    _INTEGRITY_SELECT = ' UNION '.join(
        'SELECT {0} sw_graphic, first_language, survey_language FROM naming_unit WHERE {0} IS NOT NULL'.format(
            'sw{}_graphic'.format(i+1)
        ) for i in range(4)
    )
    # SELECT sw1_graphic sw_graphic, first_language, survey_language from naming_unit WHERE sw1_graphic is not null
    # UNION SELECT sw2_graphic, first_language, survey_language from naming_unit WHERE sw2_graphic is not null
    # UNION SELECT sw3_graphic, first_language, survey_language from naming_unit WHERE sw3_graphic is not null
    # UNION SELECT sw4_graphic, first_language, survey_language from naming_unit WHERE sw4_graphic is not null

    def generate(self, force, **kwargs) -> int:
        if kwargs['corpus']:
            with sk.Corpus(configuration.CORPUS_FILE) as corpus:
                SourceWord.CORPUS = corpus
                affected = self._generate(force, SourceWord)
                SourceWord.CORPUS = None
            return affected
        else:
            return self._generate(force, SourceWord)


class SplinterTable(Table):
    _NAME = 'splinter'
    _FIELDS = ('nu_graphic', 'first_language', 'survey_language', 'image_id', 'type_of_splinter',
               'sw1_splinter', 'sw2_splinter', 'sw3_splinter', 'sw4_splinter',
               'sw1_splinter_len', 'sw2_splinter_len', 'sw3_splinter_len', 'sw4_splinter_len',
               'G_sw1_splinter', 'G_sw1_splinter__ignore', 'G_sw2_splinter', 'G_sw2_splinter__ignore',
               'G_sw3_splinter', 'G_sw3_splinter__ignore', 'G_sw4_splinter', 'G_sw4_splinter__ignore',
               'G_sw1_splinter_len', 'G_sw1_splinter_len__ignore', 'G_sw2_splinter_len', 'G_sw2_splinter_len__ignore',
               'G_sw3_splinter_len', 'G_sw3_splinter_len__ignore', 'G_sw4_splinter_len', 'G_sw4_splinter_len__ignore')
    _PRIMARY = 5

    _INTEGRITY_SELECT = "SELECT {} FROM naming_unit, ({}) T".format(
        ', '.join(_FIELDS[:_PRIMARY]),
        ' UNION '.join(
            'SELECT \'{}\' type_of_splinter'.format(t) for t in (
                'graphic strict',
                'graphic modified',
                'phonetic strict',
                'phonetic modified'
            )
        )
    )
    # SELECT nu_graphic, first_language, survey_language, image_id, type_of_splinter FROM naming_unit,
    #   (SELECT 'graphic strict' type_of_splinter
    # UNION SELECT 'graphic modified' type_of_splinter
    # UNION SELECT 'phonetic strict' type_of_splinter
    # UNION SELECT 'phonetic modified' type_of_splinter) T;

    _GENERATE_SELECT_ALL = """
SELECT
  SPL.*, NU.nu_phonetic, NU.sw1_graphic, NU.sw2_graphic, NU.sw3_graphic, NU.sw4_graphic,
  SW1.sw_phonetic sw1_phonetic, SW2.sw_phonetic sw2_phonetic, SW3.sw_phonetic sw3_phonetic, SW4.sw_phonetic sw4_phonetic
FROM splinter SPL
  LEFT JOIN naming_unit NU
    ON NU.nu_graphic=SPL.nu_graphic AND NU.first_language=SPL.first_language AND
       NU.survey_language=SPL.survey_language AND NU.image_id=SPL.image_id
  LEFT JOIN source_word SW1
    ON SW1.sw_graphic=NU.sw1_graphic AND
       SW1.first_language=SPL.first_language AND SW1.survey_language=SPL.survey_language
  LEFT JOIN source_word SW2
    ON SW2.sw_graphic=NU.sw2_graphic AND
       SW2.first_language=SPL.first_language AND SW2.survey_language=SPL.survey_language
  LEFT JOIN source_word SW3
    ON SW3.sw_graphic=NU.sw3_graphic AND
       SW3.first_language=SPL.first_language AND SW3.survey_language=SPL.survey_language
  LEFT JOIN source_word SW4
    ON SW4.sw_graphic=NU.sw4_graphic AND
       SW4.first_language=SPL.first_language AND SW4.survey_language=SPL.survey_language
"""

    _GENERATE_SELECT_NEEDED = _GENERATE_SELECT_ALL + """
WHERE
  SPL.type_of_splinter LIKE 'graphic %' AND (
    SPL.G_sw1_splinter IS NULL AND SW1.sw_graphic IS NOT NULL
    OR SPL.G_sw2_splinter IS NULL AND SW2.sw_graphic IS NOT NULL
    OR SPL.G_sw3_splinter IS NULL AND SW3.sw_graphic IS NOT NULL
    OR SPL.G_sw4_splinter IS NULL AND SW4.sw_graphic IS NOT NULL
  ) OR SPL.type_of_splinter LIKE 'phonetic %' AND (
    SPL.G_sw1_splinter IS NULL AND SW1.sw_phonetic IS NOT NULL
    OR SPL.G_sw2_splinter IS NULL AND SW2.sw_phonetic IS NOT NULL
    OR SPL.G_sw3_splinter IS NULL AND SW3.sw_phonetic IS NOT NULL
    OR SPL.G_sw4_splinter IS NULL AND SW4.sw_phonetic IS NOT NULL
  )
"""

    def generate(self, force, **kwargs) -> int:
        return self._generate(force, Splinter)


class SplinterView(EditableTableLike):

    _NAME = 'splinter_view'

    _PRIMARY = 4

    _EXCLUDE_EDITABLE = {
        'gs_name',
        'gm_name',
        'ps_name',
        'pm_name',
    }

    __NU_FIELDS_ALL = __NU_FIELDS = (
        'nu_graphic', 'first_language', 'survey_language', 'image_id',
        'wf_process',

        # 'sw1_graphic', 'sw2_graphic', 'sw3_graphic', 'sw4_graphic',
        # 'sw1_headmod', 'sw2_headmod', 'sw3_headmod', 'sw4_headmod',
        # 'sw1_subdom', 'sw2_subdom', 'sw3_subdom', 'sw4_subdom',

        'nu_word_class', 'nu_phonetic',
        'nu_syllabic', 'G_nu_syllabic', 'G_nu_syllabic__ignore',
        'nu_graphic_len', 'G_nu_graphic_len',
        'nu_phonetic_len', 'G_nu_phonetic_len',
        'nu_syllabic_len', 'G_nu_syllabic_len',
        'n_of_overlapping_letters', 'G_n_of_overlapping_letters',
        'n_of_overlapping_phones', 'G_n_of_overlapping_phones',
        'lexsh_main', 'G_lexsh_main', 'G_lexsh_main__ignore', 'lexsh_sm', 'G_lexsh_sm', 'G_lexsh_sm__ignore',
        'lexsh_whatm', 'G_lexsh_whatm', 'G_lexsh_whatm__ignore',
        'split_point_1', 'G_split_point_1', 'split_point_2', 'G_split_point_2', 'split_point_3', 'G_split_point_3'
    )

    __IMG_FIELDS = (
        'sub_sem_cat', 'dom_sem_cat', 'sub_name', 'dom_name',
        'sub_number', 'dom_number', 'half_number', 'sub_sub'
    )

    __SW_FIELDS = (
        'sw_graphic',
        'source_language', 'sw_phonetic', 'sw_word_class',
        'sw_syllabic', 'G_sw_syllabic', 'G_sw_syllabic__ignore',
        'sw_graphic_len', 'G_sw_graphic_len',
        'sw_phonetic_len', 'G_sw_phonetic_len',
        'sw_syllabic_len', 'G_sw_syllabic_len', 'frequency_in_snc'
    )

    __SPL_FIELDS_ALL = (
        'nu_graphic', 'first_language', 'survey_language', 'image_id',
        'type_of_splinter',
        'sw1_splinter', 'sw2_splinter', 'sw3_splinter', 'sw4_splinter',
        'sw1_splinter_len', 'sw2_splinter_len', 'sw3_splinter_len', 'sw4_splinter_len',
        'G_sw1_splinter', 'G_sw1_splinter__ignore', 'G_sw2_splinter', 'G_sw2_splinter__ignore',
        'G_sw3_splinter', 'G_sw3_splinter__ignore', 'G_sw4_splinter', 'G_sw4_splinter__ignore',
        'G_sw1_splinter_len', 'G_sw1_splinter_len__ignore', 'G_sw2_splinter_len', 'G_sw2_splinter_len__ignore',
        'G_sw3_splinter_len', 'G_sw3_splinter_len__ignore', 'G_sw4_splinter_len', 'G_sw4_splinter_len__ignore'
    )
    __SPL_FIELDS_EXTRA = {'nu_graphic', 'first_language', 'survey_language', 'image_id'}

    __SPL_TYPES = ('gs', 'gm', 'ps', 'pm')

    def __init__(self, wb, conn):

        self.__SPL_FIELDS = tuple(f for f in self.__SPL_FIELDS_ALL if f not in self.__SPL_FIELDS_EXTRA)

        self._FIELDS, static_fields, select_fields = self.__create_fields()
        self._EXCLUDE_EDITABLE.update(static_fields)
        self._EXPORT_SELECT = self.__create_export_select(select_fields)

        super().__init__(wb, conn)  # vyzaduje _FIELDS

        self.__nu_table = NamingUnitTable(wb, conn, self.__NU_FIELDS_ALL)
        self.__spl_table = SplinterTable(wb, conn, self.__SPL_FIELDS_ALL)

        self.__indices = self.__create_indices()  # splinter indices

    def __create_fields(self):

        def sw_fn(f: str) -> str:
            gflag = f.startswith('G_')
            if gflag:
                f = f[2:]
            if f.startswith('sw_'):
                f = f[3:]
            return 'G_sw{}_' + f if gflag else 'sw{}_' + f

        def spl_fn(f: str) -> str:
            if f == 'type_of_splinter':
                return '{}_name'
            gflag = f.startswith('G_')
            if gflag:
                f = f[2:]
            return 'G_{}_' + f if gflag else '{}_' + f

        fields = []
        static = []  # img, sw
        select = []

        fields.extend(self.__NU_FIELDS)
        select.extend('NU.' + f for f in self.__NU_FIELDS)

        fields.extend(self.__IMG_FIELDS)
        static.extend(self.__IMG_FIELDS)
        select.extend('I.' + f for f in self.__IMG_FIELDS)

        sw_fmt = [sw_fn(f) for f in self.__SW_FIELDS]

        for i in range(4):
            for field, fmt in zip(self.__SW_FIELDS, sw_fmt):
                newname = fmt.format(i+1)
                fields.append(newname)
                static.append(newname)
                select.append('SW{}.{} {}'.format(i+1, field, newname))

        spl_fmt = [spl_fn(f) for f in self.__SPL_FIELDS]

        for name in self.__SPL_TYPES:
            upcase = name.upper()
            for field, fmt in zip(self.__SPL_FIELDS, spl_fmt):
                newname = fmt.format(name)
                fields.append(newname)
                select.append('{}.{} {}'.format(upcase, field, newname))

        return tuple(fields), tuple(static), tuple(select)

    @staticmethod
    def __create_export_select(select_fields):
        return """SELECT {} FROM naming_unit NU

  LEFT JOIN image I
    ON NU.image_id = I.image_id

  LEFT JOIN source_word SW1
    ON NU.first_language = SW1.first_language
       AND NU.survey_language = SW1.survey_language
       AND NU.sw1_graphic = SW1.sw_graphic
  LEFT JOIN source_word SW2
    ON NU.first_language = SW2.first_language
       AND NU.survey_language = SW2.survey_language
       AND NU.sw2_graphic = SW2.sw_graphic
  LEFT JOIN source_word SW3
    ON NU.first_language = SW3.first_language
       AND NU.survey_language = SW3.survey_language
       AND NU.sw3_graphic = SW3.sw_graphic
  LEFT JOIN source_word SW4
    ON NU.first_language = SW4.first_language
       AND NU.survey_language = SW4.survey_language
       AND NU.sw4_graphic = SW4.sw_graphic

  LEFT JOIN splinter GS
    ON NU.nu_graphic = GS.nu_graphic
      AND NU.first_language = GS.first_language
      AND NU.survey_language = GS.survey_language
      AND NU.image_id = GS.image_id
      AND GS.type_of_splinter = 'graphic strict'

  LEFT JOIN splinter GM
    ON NU.nu_graphic = GM.nu_graphic
      AND NU.first_language = GM.first_language
      AND NU.survey_language = GM.survey_language
      AND NU.image_id = GM.image_id
      AND GM.type_of_splinter = 'graphic modified'

  LEFT JOIN splinter PS
    ON NU.nu_graphic = PS.nu_graphic
      AND NU.first_language = PS.first_language
      AND NU.survey_language = PS.survey_language
      AND NU.image_id = PS.image_id
      AND PS.type_of_splinter = 'phonetic strict'

  LEFT JOIN splinter PM
    ON NU.nu_graphic = PM.nu_graphic
      AND NU.first_language = PM.first_language
      AND NU.survey_language = PM.survey_language
      AND NU.image_id = PM.image_id
      AND PM.type_of_splinter = 'phonetic modified';
""".format(
            ', '.join(select_fields)
        )

    def __create_indices(self):

        def spl_range(name):
            nu = len(self.__NU_FIELDS)
            img = len(self.__IMG_FIELDS)
            sw = len(self.__SW_FIELDS)
            spl = len(self.__SPL_FIELDS)
            start = nu + img + 4 * sw + self.__SPL_TYPES.index(name) * spl
            return range(start, start + spl)

        extending = [self._FIELDS.index(ef) for ef in self.__SPL_FIELDS_EXTRA]
        return {name: sorted(list(spl_range(name)) + extending) for name in self.__SPL_TYPES}

    def _update(self, datarow):
        self.__nu_table._update([datarow[i] for i in range(len(self.__NU_FIELDS))])
        for name in self.__SPL_TYPES:
            self.__spl_table._update([datarow[i] for i in self.__indices[name]])

    @property
    def integrity_kept(self) -> bool:
        query = """SELECT COUNT(*) FROM naming_unit NU
  LEFT JOIN splinter GS
    ON NU.nu_graphic = GS.nu_graphic
      AND NU.first_language = GS.first_language
      AND NU.survey_language = GS.survey_language
      AND NU.image_id = GS.image_id
      AND GS.type_of_splinter = 'graphic strict'

  LEFT JOIN splinter GM
    ON NU.nu_graphic = GM.nu_graphic
      AND NU.first_language = GM.first_language
      AND NU.survey_language = GM.survey_language
      AND NU.image_id = GM.image_id
      AND GM.type_of_splinter = 'graphic modified'

  LEFT JOIN splinter PS
    ON NU.nu_graphic = PS.nu_graphic
      AND NU.first_language = PS.first_language
      AND NU.survey_language = PS.survey_language
      AND NU.image_id = PS.image_id
      AND PS.type_of_splinter = 'phonetic strict'

  LEFT JOIN splinter PM
    ON NU.nu_graphic = PM.nu_graphic
      AND NU.first_language = PM.first_language
      AND NU.survey_language = PM.survey_language
      AND NU.image_id = PM.image_id
      AND PM.type_of_splinter = 'phonetic modified'

  WHERE GS.type_of_splinter IS NULL OR GM.type_of_splinter IS NULL
    OR PS.type_of_splinter IS NULL OR PM.type_of_splinter IS NULL"""

        return self._execute(query).cursor.fetchone()[0] == 0
