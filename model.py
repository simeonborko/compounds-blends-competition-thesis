from abc import ABC, ABCMeta, abstractmethod
import sys
from collections import namedtuple

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from pymysql.cursors import DictCursor
from syllabiky.syllabiky import split_phrase
from syllabiky.DbMatcher import DbMatcher
import configuration
from tools import sk, en


class TableLike(ABC):

    _NAME = None
    _FIELDS = None
    _PRIMARY = None  # pocet stlpcov zo zaciatku
    _EXPORT_SELECT = None

    _REDFILL = PatternFill("solid", fgColor="FF7575")
    _YELLOWFILL = PatternFill("solid", fgColor="FFFC75")

    ExecuteResult = namedtuple('ExecuteResult', ['cursor', 'result'])

    def __init__(self, wb: Workbook, conn):
        self._wb = wb
        self.__conn = conn

    def __add_header(self, sheet):
        sheet.append(self._FIELDS)
        sheet.row_dimensions[1].font = Font(bold=True)
        for i in range(self._PRIMARY):
            sheet.cell(row=1, column=i + 1).font = Font(bold=True, italic=True)

    def _execute(self, *args, **kwargs) -> ExecuteResult:
        c = self.__conn.cursor(**kwargs)
        res = c.execute(*args) or 0
        return self.ExecuteResult(c, res)

    def _executemany(self, *args, **kwargs) -> ExecuteResult:
        c = self.__conn.cursor(**kwargs)
        res = c.executemany(*args) or 0
        return self.ExecuteResult(c, res)

    @abstractmethod
    def _sync(self, vals_gen):
        """
        Synchronizuje dane riadky.
        :param vals_gen: generator na dvojice (zoznam hodnot v DB, zoznam Cell v SHEETE)
        """
        pass

    def create_sheet(self) -> bool:
        if self._NAME in self._wb.sheetnames:
            return False

        sheet = self._wb.create_sheet(self._NAME)

        # nadpisy
        self.__add_header(sheet)

        # data
        for row in self._execute(self._EXPORT_SELECT).cursor:
            sheet.append(row)

        return True

    def sync(self):
        # ziskat zaznamy z DB
        db_dict = {dbvals[:self._PRIMARY]: dbvals for dbvals in self._execute(self._EXPORT_SELECT).cursor}

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

        # co su iba v DB, pridat zlto
        if len(keys_db_only) > 0:
            starting_row = sheet.max_row + 1
            for key in keys_db_only:
                sheet.append(db_dict[key])
            for row in sheet.iter_rows(min_row=starting_row):
                for cell in row:
                    cell.fill = self._YELLOWFILL

        # co su iba v SHEET, ofarbit cerveno
        for key in keys_sheet_only:
            for cell in sheet_dict[key]:
                cell.fill = self._REDFILL

        # co su aj aj, synchronizovat, zafarbit zlto zmenene
        self._sync((db_dict[k], sheet_dict[k]) for k in keys_both)

    @classmethod
    def primary_fields(cls):
        return cls._FIELDS[:cls._PRIMARY]

    @classmethod
    def name(cls) -> str: return cls._NAME


class StaticView(TableLike):

    def _sync(self, vals_gen):
        """Nahradi hodnoty v SHEETE hodnotami z DB"""
        for db_values, sheet_cells in vals_gen:
            for value, cell in zip(db_values, sheet_cells):
                if value and cell.value != value:
                    cell.value = value
                    cell.fill = self._YELLOWFILL


class EditableTableLike(TableLike):

    _ALLOWED_TO_GENERATE = None

    def _sync(self, vals_gen):
        editable, generated = self._split_fields()

        for db_values, sheet_cells in vals_gen:

            modified = False
            for i in editable:
                if db_values[i] != sheet_cells[i].value:
                    db_values[i] = sheet_cells[i].value
            if modified:
                self._update(db_values)

            for i in generated:
                if db_values[i] != sheet_cells[i].value:
                    sheet_cells[i].value = db_values[i]
                    sheet_cells[i].fill = self._YELLOWFILL

    @abstractmethod
    def _update(self, datarow):
        pass

    @classmethod
    def _split_fields(cls) -> (tuple, tuple):
        """Rozdeli stlpce podla toho, ci su editovatelne alebo generovane"""
        editable = []
        generated = []
        for i, field in enumerate(cls._FIELDS[cls._PRIMARY:], cls._PRIMARY):
            if field[:2] == 'G_' and field[-8:] != '__ignore' or \
                    cls._ALLOWED_TO_GENERATE is not None and field in cls._ALLOWED_TO_GENERATE:
                generated.append(i)
            else:
                editable.append(i)
        return tuple(editable), tuple(generated)

    @classmethod
    def generated_fields(cls) -> tuple:
        return tuple(cls._FIELDS[i] for i in cls._split_fields()[1])


class Table(EditableTableLike, metaclass=ABCMeta):

    # select iba na tie riadky, ktore potrebuju byt generovane
    _GENERATE_SELECT = None

    # select na riadky, ake primarne kluce maju byt v danej tabulke
    _INTEGRITY_SELECT = None

    def __init__(self, wb: Workbook, conn):
        super().__init__(wb, conn)
        self._GENERATE_SELECT = "SELECT {} FROM {}".format(','.join(self._FIELDS), self._NAME)

    def _update(self, datarow):
        query = "UPDATE {} SET {} WHERE {}".format(
            self._NAME,
            ', '.join(f + " = %s" for f in self._FIELDS[self._PRIMARY:]),
            ' AND '.join(f + " = %s" for f in self._FIELDS[:self._PRIMARY])
        )
        data = datarow[self._PRIMARY:] + datarow[:self._PRIMARY]
        self._execute(query, data)

    def _generate(self, force: bool, cls) -> int:

        # TODO: chcelo by to nepouzivat dict, ale named tuple

        c = self._execute(
            "SELECT * FROM {}".format(self._NAME) if force else self._GENERATE_SELECT,
            cursor=DictCursor
        ).cursor

        args = []

        for data in c:
            entity = cls(data)
            entity.generate()
            if entity.modified:
                args.append(entity.data)

        if len(args):

            query = "UPDATE {} SET {} WHERE {}".format(
                self._NAME,
                ", ".join("{0}=%({0})s".format(g) for g in self.generated_fields()),
                " AND ".join("{0}=%({0})s".format(p) for p in self.primary_fields())
            )

            affected = self._executemany(query, args, result=True).result

            if len(args) != affected:
                print("Pocet args: {}, pocet affected: {}".format(len(args), affected), file=sys.stderr)

            return affected

        else:
            return 0

    def integrity_add(self) -> int:
        return self._execute(
            "INSERT IGNORE INTO {} ({}) {}".format(
                self._NAME,
                ', '.join(self.primary_fields()),
                self._INTEGRITY_SELECT
            ),
            result=True
        ).result

    def integrity_junk(self) -> int:
        exres = self._execute(
            "SELECT {} FROM {} TBL LEFT JOIN ({}) TMP ON {} WHERE {}".format(
                ', '.join('TBL.' + field for field in self._FIELDS),
                self._NAME,
                self._INTEGRITY_SELECT,
                ' AND '.join('TBL.{0} = TMP.{0}'.format(p) for p in self.primary_fields()),
                ' AND '.join('TMP.{} IS NULL'.format(p) for p in self.primary_fields())
            )
        )
        if not exres.result:
            return 0

        # vytvorit harok
        sheetname = 'junk {}'.format(self._NAME)
        if sheetname not in self._wb.sheetnames:
            sheet = self._wb.create_sheet(sheetname)
            self.__add_header(sheet)
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
                ' AND '.join('{} = %s'.format(p) for p in self.primary_fields())
            ),
            keys
        )
        return exres.result


class SplinterView(EditableTableLike):
    pass


class ImageTable(Table):
    _NAME = 'image'
    _FIELDS = ('image_id', 'sub_sem_cat', 'dom_sem_cat', 'sub_name', 'dom_name', 'sub_number', 'dom_number', 'half_number', 'sub_sub')
    _PRIMARY = 1


class LanguageTable(Table):
    _NAME = 'language'
    _FIELDS = ('code', 'name')
    _PRIMARY = 1
    _INTEGRITY_SELECT = "SELECT first_language code FROM respondent UNION SELECT survey_language code FROM respondent"


class NamingUnitTable(Table):
    _NAME = 'naming_unit'
    _FIELDS = ('nu_graphic', 'first_language', 'survey_language', 'image_id',
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
               'split_point_1', 'G_split_point_1', 'split_point_2', 'G_split_point_2', 'split_point_3', 'G_split_point_3')
    _PRIMARY = 4

    _GENERATE_SELECT = """select * from {} where
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
    _FIELDS = ('respondent_id', 'first_language', 'survey_language', 'first_language_original', 'second_language', 'other_language', 'age', 'sex', 'sex_original', 'employment', 'education', 'birth_place', 'year_of_birth', 'responding_date')
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
    _ALLOWED_TO_GENERATE = ('frequency_in_snc',)
    _GENERATE_SELECT = """select * from {} where
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
    _FIELDS = ('nu_graphic', 'first_language', 'survey_language', 'image_id', 'type_of_splinter', 'sw1_splinter', 'sw2_splinter', 'sw3_splinter', 'sw4_splinter', 'sw1_splinter_len', 'sw2_splinter_len', 'sw3_splinter_len', 'sw4_splinter_len', 'G_sw1_splinter', 'G_sw1_splinter__ignore', 'G_sw2_splinter', 'G_sw2_splinter__ignore', 'G_sw3_splinter', 'G_sw3_splinter__ignore', 'G_sw4_splinter', 'G_sw4_splinter__ignore', 'G_sw1_splinter_len', 'G_sw1_splinter_len__ignore', 'G_sw2_splinter_len', 'G_sw2_splinter_len__ignore', 'G_sw3_splinter_len', 'G_sw3_splinter_len__ignore', 'G_sw4_splinter_len', 'G_sw4_splinter_len__ignore')
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


class Entity:

    _TABLE_CLS = None

    def __init__(self, data: dict):
        self.__data = data
        self.__modified = False
        self.__primary_fields = self._TABLE_CLS.primary_fields()

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        if key in self.__primary_fields:
            raise Exception('Hodnota v stlpci patriacom do primarneho kluca nemoze byt zmenena')
        if self.__data[key] != value:
            self.__data[key] = value
            self.__modified = True

    @property
    def data(self) -> dict:
        """Vrati data, ktore mozu byt generovane alebo patria do primarneho kluca"""
        fields = self.__primary_fields + self._TABLE_CLS.generated_fields()
        return {k: v for k, v in self.__data.items() if k in fields}

    @property
    def modified(self) -> bool:
        return self.__modified

    def generate(self):
        raise NotImplementedError


class SourceWord(Entity):

    CORPUS = None  # corpus ma nastavit volajuci
    _TABLE_CLS = SourceWordTable
    __MATCHER = DbMatcher()

    def __init__(self, data: dict):
        super().__init__(data)
        self.__lang = self['survey_language']

    def __sw_syllabic(self):
        if self.__lang == 'SK':
            newval = None
            try:
                newval = split_phrase(self['sw_graphic'], self.__MATCHER)
            except TypeError:
                print("TypeError split_phrase:", self['sw_graphic'])
            self['G_sw_syllabic'] = newval

    def __sw_graphic_len(self):
        if self.__lang == 'SK':
            self['G_sw_graphic_len'] = sk.count_letters(self['sw_graphic'])
        elif self.__lang == 'EN':
            self['G_sw_graphic_len'] = en.count_letters(self['sw_graphic'])

    def __sw_phonetic_len(self):
        if self['sw_phonetic']:
            if self.__lang == 'SK':
                self['G_sw_phonetic_len'] = sk.count_phones(self['sw_phonetic'])
            elif self.__lang == 'EN':
                self['G_sw_phonetic_len'] = en.count_phones(self['sw_phonetic'])
        else:
            self['G_sw_phonetic_len'] = None

    def __sw_syllabic_len(self):
        """najprv zavolat self.__sw_syllabic()"""
        newval = None
        if self.__lang == 'SK' and self['G_sw_syllabic']:
            newval = self['G_sw_syllabic'].count('-') + 1
        elif self.__lang == 'EN' and self['sw_phonetic']:
            newval = en.count_syllables(self['sw_phonetic'])
        self['G_sw_syllabic_len'] = newval

    def __frequency_in_snc(self):
        if self.__lang == 'SK' and self.CORPUS is not None:
            self['frequency_in_snc'] = self.CORPUS.get_frequency(self['sw_graphic'])

    def generate(self):
        self.__sw_syllabic()
        self.__sw_graphic_len()
        self.__sw_phonetic_len()
        self.__sw_syllabic_len()
        self.__frequency_in_snc()


class NamingUnit(Entity):

    _TABLE_CLS = NamingUnitTable
    __MATCHER = DbMatcher()

    def __init__(self, data: dict):
        super().__init__(data)
        self.__lang = self['survey_language']

    def __nu_syllabic(self):
        if self.__lang == 'SK':
            newval = None
            try:
                newval = split_phrase(self['nu_graphic'], self.__MATCHER)
            except TypeError:
                print("TypeError split_phrase:", self['nu_graphic'])
            self['G_nu_syllabic'] = newval

    def __nu_graphic_len(self):
        if self.__lang == 'SK':
            self['G_nu_graphic_len'] = sk.count_letters(self['nu_graphic'])
        elif self.__lang == 'EN':
            self['G_nu_graphic_len'] = en.count_letters(self['nu_graphic'])

    def __nu_phonetic_len(self):
        if self['nu_phonetic']:
            if self.__lang == 'SK':
                self['G_nu_phonetic_len'] = sk.count_phones(self['nu_phonetic'])
            elif self.__lang == 'EN':
                self['G_nu_phonetic_len'] = en.count_phones(self['nu_phonetic'])
        else:
            self['G_nu_phonetic_len'] = None

    def __nu_syllabic_len(self):
        newval = None
        if self.__lang == 'SK' and self['G_nu_syllabic']:
            newval = self['G_nu_syllabic'].count('-') + 1
        elif self.__lang == 'EN' and self['nu_phonetic']:
            newval = en.count_syllables(self['nu_phonetic'])
        self['G_nu_syllabic_len'] = newval

    # def __n_of_overlapping_letters(self):
    #     pass
    #
    # def __n_of_overlapping_phones(self):
    #     pass
    #
    # def __lexsh_main(self):
    #     pass
    #
    # def __lexsh_sm(self):
    #     pass
    #
    # def __lexsh_whatm(self):
    #     pass
    #
    # def __split_point_1(self):
    #     pass
    #
    # def __split_point_2(self):
    #     pass
    #
    # def __split_point_3(self):
    #     pass

    def generate(self):
        self.__nu_syllabic()
        self.__nu_graphic_len()
        self.__nu_phonetic_len()
        self.__nu_syllabic_len()





