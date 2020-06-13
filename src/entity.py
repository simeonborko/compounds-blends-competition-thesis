from abc import abstractmethod, ABC
from typing import Optional, Type, Tuple

from syllabiky.syllabiky import split_phrase
from syllabiky.DbMatcher import DbMatcher
from src.tools import en
from src.tools import sk
from src.tools.exception import WordSegmentException
from src.tools.overlapable import get_overlapable
from src.tools.splinter import SlovakGraphicSplinter, SlovakPhoneticSplinter, EnglishGraphicSplinter, \
    EnglishPhoneticSplinter, Overlap, LexshType, parse_lexsh_type, GraphicSplinter
from src.tools.corpora import SlovakExactCorpus, SlovakSubstringCorpus, EnglishExactCorpus, EnglishSubstringCorpus


class Entity(ABC):

    def __init__(self, table, data: dict):
        self.__table = table
        self.__data = data
        self.__modified = False

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        if key in self.__table.primary_fields:
            raise Exception('Hodnota v stlpci patriacom do primarneho kluca nemoze byt zmenena')
        if self.__data[key] != value:
            self.__data[key] = value
            self.__modified = True

    def get_generated(self, item):
        """Ak je item aj generovany aj editovatelny, tak primarne vrati editovatelny, inak generovany"""
        res = self[item]
        if not res:
            res = self[f'G_{item}']
        return res

    @property
    def data(self) -> dict:
        """Vrati data, ktore mozu byt generovane alebo patria do primarneho kluca"""
        fields = self.__table.generated_fields.union(self.__table.primary_fields)
        return {k: v for k, v in self.__data.items() if k in fields}

    @property
    def modified(self) -> bool:
        return self.__modified

    @abstractmethod
    def generate(self):
        pass


class SourceWord(Entity):

    CORPUS: Optional[SlovakExactCorpus] = None  # corpus ma nastavit volajuci
    BNC_CORPUS: Optional[EnglishExactCorpus] = None  # ma nastavit volajuci
    TRANSCRIPTION_MANAGER = None  # ma nastavit volajuci
    __MATCHER = DbMatcher()

    def __init__(self, table, data: dict):
        super().__init__(table, data)
        self.__lang = self['survey_language']
        self.__src_lang_sk = self['source_language'] != 'EN'

    def __sw_phonetic(self):
        if self.TRANSCRIPTION_MANAGER is not None:
            self['G_sw_phonetic'] = self.TRANSCRIPTION_MANAGER[self['sw_graphic']] if self.__lang == 'EN' else 'NA'

    def __sw_syllabic(self):
        if self.__lang == 'SK':
            newval = None
            if self.__src_lang_sk:
                try:
                    newval = split_phrase(self['sw_graphic'], self.__MATCHER)
                except TypeError:
                    print("TypeError split_phrase:", self['sw_graphic'])
        else:
            newval = 'NA'
        self['G_sw_syllabic'] = newval

    def __sw_graphic_len(self):
        if self.__lang == 'SK':
            self['G_sw_graphic_len'] = sk.count_letters(self['sw_graphic'], self.__src_lang_sk)
        elif self.__lang == 'EN':
            self['G_sw_graphic_len'] = en.count_letters(self['sw_graphic'])

    def __sw_phonetic_len(self):
        newval = None
        if self['sw_phonetic']:
            try:
                if self.__lang == 'SK':
                    newval = sk.count_phones(self['sw_phonetic'])
                elif self.__lang == 'EN':
                    newval = en.count_phones(self['sw_phonetic'])
            except WordSegmentException:
                pass
        self['G_sw_phonetic_len'] = newval

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
        elif self.__lang == 'EN' and self.BNC_CORPUS is not None:
            self['frequency_in_snc'] = self.BNC_CORPUS.get_frequency(self['sw_graphic'])

    def generate(self):
        self.__sw_phonetic()
        self.__sw_syllabic()
        self.__sw_graphic_len()
        self.__sw_phonetic_len()
        self.__sw_syllabic_len()
        self.__frequency_in_snc()


class NamingUnit(Entity):

    CORPUS_SK: Optional[SlovakExactCorpus] = None  # corpus ma nastavit volajuci
    CORPUS_EN: Optional[EnglishExactCorpus] = None  # ma nastavit volajuci
    SPLINTER_DERIVED: Optional[bool] = None  # SPLINTER_DERIVED ma nastavit volajuci
    __MATCHER = DbMatcher()

    def __init__(self, table, data: dict):
        super().__init__(table, data)
        self.__lang = self['survey_language']
        if self.__lang not in ('SK', 'EN'):
            raise Exception
        self.__nu_src_lang_sk = _is_slovak(self['nu_source_language'])

    def __nu_syllabic(self):
        if self.__lang == 'SK':
            newval = None
            try:
                newval = split_phrase(self['nu_graphic'], self.__MATCHER)
            except TypeError:
                print("TypeError split_phrase:", self['nu_graphic'])
        else:
            newval = 'NA'
        self['G_nu_syllabic'] = newval

    def __nu_graphic_len(self):
        if self.__lang == 'SK':
            self['G_nu_graphic_len'] = sk.count_letters(self['nu_graphic'], self.__nu_src_lang_sk)
        elif self.__lang == 'EN':
            self['G_nu_graphic_len'] = en.count_letters(self['nu_graphic'])

    def __nu_phonetic_len(self):
        newval = None
        if self['nu_phonetic']:
            try:
                if self.__lang == 'SK':
                    newval = sk.count_phones(self['nu_phonetic'])
                elif self.__lang == 'EN':
                    newval = en.count_phones(self['nu_phonetic'])
            except WordSegmentException:
                pass
        self['G_nu_phonetic_len'] = newval

    def __nu_syllabic_len(self):
        newval = None
        if self.__lang == 'SK' and self['G_nu_syllabic']:
            newval = self['G_nu_syllabic'].count('-') + 1
        elif self.__lang == 'EN' and self['nu_phonetic']:
            newval = en.count_syllables(self['nu_phonetic'])
        self['G_nu_syllabic_len'] = newval
        
    def __nu_corpus_frequency(self):
        if self.__lang == 'SK' and self.CORPUS_SK is not None:
            self['G_nu_corpus_frequency'] = self.CORPUS_SK.get_frequency(self['nu_graphic'])
        elif self.__lang == 'EN' and self.CORPUS_EN is not None:
            self['G_nu_corpus_frequency'] = self.CORPUS_EN.get_frequency(self['nu_graphic'])

    def __lexsh(self):

        cls: Type[GraphicSplinter] = SlovakGraphicSplinter if self.__lang == 'SK' else EnglishGraphicSplinter

        lexsh_main = []
        is_lexsh_modified = False
        lexsh_whatm = []

        for i in range(4):
            sw_graphic = self[f'sw{i+1}_graphic']
            J_gs_splinter = self[f'J_gs_sw{i+1}_splinter']
            G_gs_splinter = self[f'G_gs_sw{i+1}_splinter']
            J_gm_splinter = self[f'J_gm_sw{i+1}_splinter']
            G_gm_splinter = self[f'G_gm_sw{i+1}_splinter']
            if not sw_graphic or not J_gs_splinter or sw_graphic in ('NA', 'N/A'):
                # if we don't have source word or splinter, then break
                break

            lexsh_main_item: Optional[Tuple[str, bool]] = None
            lexsh_whatm_item: Optional[Tuple[str, bool]] = None

            splinter_obj = cls(self['nu_graphic'], sw_graphic, True, nu_src_lang_sk=self.__nu_src_lang_sk)
            _, used_splinter, warning = splinter_obj.set_splinter_preferably(J_gs_splinter, G_gs_splinter)
            lexsh = splinter_obj.lexical_shortening

            if lexsh:
                lexsh_main_item = (lexsh.name, warning)
                if J_gm_splinter:
                    if used_splinter in (J_gm_splinter, G_gm_splinter):
                        lexsh_whatm_item = lexsh_main_item
                    else:
                        is_lexsh_modified = True
                        splinter_obj = cls(self['nu_graphic'], sw_graphic, False, nu_src_lang_sk=self.__nu_src_lang_sk)
                        _, _, warning = splinter_obj.set_splinter_preferably(J_gm_splinter, G_gm_splinter)
                        lexsh = splinter_obj.lexical_shortening
                        if lexsh:
                            lexsh_whatm_item = (f'{lexsh.name}m', warning)

            for lst, item in zip((lexsh_main, lexsh_whatm), (lexsh_main_item, lexsh_whatm_item)):
                to_append = item[0]
                if item[1]:
                    to_append += '_warn'
                lst.append(to_append)

        self['G_lexsh_main'] = '+'.join(lexsh_main)
        if len(lexsh_main) and len(lexsh_main) == len(lexsh_whatm):
            self['G_lexsh_sm'] = 'modified' if is_lexsh_modified else 'strict'
        else:
            self['G_lexsh_sm'] = ''
        self['G_lexsh_whatm'] = '+'.join(lexsh_whatm)

    def __overlap_segments(self, SplinterCls, graphic: bool):

        alignments = []

        gr_ph = 'graphic' if graphic else 'phonetic'
        naming_unit = self[f'nu_{gr_ph}']

        overlapping = None
        overlap_number = None

        if naming_unit:

            for i in range(4):
                source_word = self['sw{}_{}'.format(i + 1, gr_ph)]
                splinter_base_key = '{}s_sw{}_splinter'.format('g' if graphic else 'p', i + 1)
                J_splinter = self[f'J_{splinter_base_key}']
                G_splinter = self[f'G_{splinter_base_key}']
                if not source_word or not J_splinter:
                    break

                # noinspection PyUnusedLocal
                try:
                    # SplinterCls by sa mal inicializovat s jazykom zdrojoveho slova,
                    #
                    strict = SplinterCls(naming_unit, source_word, True, nu_src_lang_sk=self.__nu_src_lang_sk)
                    strict.set_splinter_preferably(J_splinter, G_splinter)
                except WordSegmentException as e:
                    # print(e, file=sys.stderr)
                    break

                if not strict.alignment:
                    break

                alignments.append(strict.alignment)

            if len(alignments):
                overlap = Overlap(naming_unit, alignments, not graphic)
                overlapping = overlap.overlapping_segments
                overlap_number = overlap.number_of_overlapping_segments

        name = 'letters' if graphic else 'phones'

        self[f'G_overlapping_{name}'] = overlapping
        self[f'G_n_of_overlapping_{name}'] = overlap_number

    def __overlap(self):
        if self.__lang == 'SK':
            self.__overlap_segments(SlovakGraphicSplinter, True)
            self.__overlap_segments(SlovakPhoneticSplinter, False)
        else:
            self.__overlap_segments(EnglishGraphicSplinter, True)
            self.__overlap_segments(EnglishPhoneticSplinter, False)

    def __get_lexsh_type(self, sw_number) -> Optional[LexshType]:
        lexsh = self.get_generated('lexsh_main')
        return parse_lexsh_type(lexsh, sw_number) if lexsh else None

    def __split_point_placement(self):
        # vyzaduje, aby bolo predtym spustene __lexsh()

        if self.__lang == 'SK':
            for N in (1, 2, 3):
                splinter_base_key = f'gs_sw{N}_splinter'
                J_splinter = self[f'J_{splinter_base_key}']
                G_splinter = self[f'G_{splinter_base_key}']
                res = None
                if self['nu_graphic'] and self[f'sw{N}_graphic'] and self[f'sw{N}_syllabic'] and J_splinter:
                    s = SlovakGraphicSplinter(self['nu_graphic'], self[f'sw{N}_graphic'], True, nu_src_lang_sk=self.__nu_src_lang_sk)
                    if s.set_splinter_preferably(J_splinter, G_splinter):
                        lexsh_type = self.__get_lexsh_type(N)
                        if lexsh_type is not None and s.lexical_shortening == lexsh_type:
                            sp = s.get_split_point(self[f'sw{N}_syllabic'])
                            if sp is not None:
                                res = str(sp)
                self[f'G_split_point_{N}'] = res

        elif self.__lang == 'EN':
            for N in (1, 2, 3):
                splinter_base_key = f'ps_sw{N}_splinter'
                J_splinter = self[f'J_{splinter_base_key}']
                G_splinter = self[f'G_{splinter_base_key}']
                res = None
                if self['nu_phonetic'] and self[f'sw{N}_phonetic'] and J_splinter:
                    s = EnglishPhoneticSplinter(self['nu_phonetic'], self[f'sw{N}_phonetic'], True, nu_src_lang_sk=self.__nu_src_lang_sk)
                    if s.set_splinter_preferably(J_splinter, G_splinter):
                        lexsh_type = self.__get_lexsh_type(N)
                        if lexsh_type is not None and s.lexical_shortening == lexsh_type:
                            sp = s.get_split_point(self[f'sw{N}_phonetic'])
                            if sp is not None:
                                res = str(sp)
                self[f'G_split_point_{N}'] = res

    def __overlapable(self):

        if self.__lang == 'SK':
            get_phones_list = sk.get_phones_list
        else:
            get_phones_list = en.get_phones_list

        if self['sw1_phonetic'] != 'NA' and self['sw2_phonetic'] != 'NA' \
                and self['sw3_phonetic'] == 'NA' and self['sw4_phonetic'] == 'NA':
            sw1 = self['sw1_phonetic']
            sw2 = self['sw2_phonetic']
            if sw1 is None or sw2 is None:
                self['G_overlapable'] = "ERROR NO PHONETIC"
                self['G_overlapable_length'] = None
                self['G_overlapable_sw1'] = None
                self['G_overlapable_sw2'] = None
                return
                
            try:
                sw1 = get_phones_list(sw1)
                sw2 = get_phones_list(sw2)
            except WordSegmentException:
                self['G_overlapable'] = "ERROR BAD PHONETIC"
                self['G_overlapable_length'] = None
                self['G_overlapable_sw1'] = None
                self['G_overlapable_sw2'] = None
                return 
                
            overlapable = get_overlapable(sw1, sw2)
            if overlapable is not None:
                self['G_overlapable'] = "YES"
                self['G_overlapable_length'] = overlapable[0]
                self['G_overlapable_sw1'] = overlapable[1] + 1
                self['G_overlapable_sw2'] = overlapable[2] + 1
            else:
                self['G_overlapable'] = "NO"
                self['G_overlapable_length'] = None
                self['G_overlapable_sw1'] = None
                self['G_overlapable_sw2'] = None

    def generate(self):
        self.__nu_syllabic()
        self.__nu_graphic_len()
        self.__nu_phonetic_len()
        self.__nu_syllabic_len()
        self.__nu_corpus_frequency()
        if self.SPLINTER_DERIVED:
            self.__lexsh()
            self.__overlap()
            self.__split_point_placement()
        self.__overlapable()


class Splinter(Entity):

    # korpusy ma nastavit volajuci
    SK_EXACT_CORPUS: Optional[SlovakExactCorpus] = None
    SK_SUBSTRING_CORPUS: Optional[SlovakSubstringCorpus] = None
    EN_EXACT_CORPUS: Optional[EnglishExactCorpus] = None
    EN_SUBSTRING_CORPUS: Optional[EnglishSubstringCorpus] = None

    def __init__(self, table, data: dict):
        super().__init__(table, data)
        self.__nu_src_lang_sk = _is_slovak(self['nu_source_language'])

    def corpus_freq(self):

        # chceme to iba pre blendy
        if self['wf_process'] != 'blend':
            return

        if self['type_of_splinter'].startswith('graphic') is False:
            return

        if self['survey_language'] == 'SK' and (self.SK_EXACT_CORPUS or self.SK_SUBSTRING_CORPUS):
            for i in range(1, 4+1):
                spl = self[f'sw{i}_splinter']
                if not spl:
                    spl = self[f'G_sw{i}_splinter']
                if not spl:
                    continue
                if self.SK_EXACT_CORPUS:
                    self[f'sw{i}_splinter_freq_exact'] = self.SK_EXACT_CORPUS.get_frequency(spl) if spl else None
                if self.SK_SUBSTRING_CORPUS:
                    self[f'sw{i}_splinter_freq_any'] = self.SK_SUBSTRING_CORPUS.get_frequency(spl) if spl else None

        elif self['survey_language'] == 'EN' and (self.EN_EXACT_CORPUS or self.EN_SUBSTRING_CORPUS):
            for i in range(1, 4+1):
                spl = self[f'sw{i}_splinter']
                if not spl:
                    spl = self[f'G_sw{i}_splinter']
                if not spl:
                    continue
                if self.EN_EXACT_CORPUS:
                    self[f'sw{i}_splinter_freq_exact'] = self.EN_EXACT_CORPUS.get_frequency(spl) if spl else None
                if self.EN_SUBSTRING_CORPUS:
                    self[f'sw{i}_splinter_freq_any'] = self.EN_SUBSTRING_CORPUS.get_frequency(spl) if spl else None

    def generate(self):
        graphic = self['type_of_splinter'].startswith('graphic')
        phonetic = self['type_of_splinter'].startswith('phonetic')
        cls = None
        if self['survey_language'] == 'SK':
            if graphic:
                cls = SlovakGraphicSplinter
            elif phonetic:
                cls = SlovakPhoneticSplinter
        elif self['survey_language'] == 'EN':
            if graphic:
                cls = EnglishGraphicSplinter
            elif phonetic:
                cls = EnglishPhoneticSplinter

        try:
            number_of_SWs = int(self['nu_number_of_SWs'])
        except ValueError:
            number_of_SWs = 2

        strict = None
        if self['type_of_splinter'].endswith('strict'):
            strict = True
        elif self['type_of_splinter'].endswith('modified'):
            strict = False

        if cls is None or strict is None:
            raise Exception

        nu = self['nu_graphic'] if graphic else self['nu_phonetic']
        if nu:
            for i in range(1, 4+1):
                sw = self['sw{}_graphic'.format(i)] if graphic else self['sw{}_phonetic'.format(i)]
                if sw:
                    splinter = ''
                    length = None

                    try:
                        s = cls(nu, sw, strict, nu_src_lang_sk=self.__nu_src_lang_sk)
                        if s.find_splinter(sw_first=(i == 1), sw_last=(i == number_of_SWs)):
                            splinter = s.splinter
                            length = s.length
                    except WordSegmentException:
                        pass

                    self['G_sw{}_splinter'.format(i)] = splinter
                    self['G_sw{}_splinter_len'.format(i)] = length

        self.corpus_freq()


def _is_slovak(src_lang):
    return not src_lang or 'SK' in src_lang or 'EN' not in src_lang
