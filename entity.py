from abc import abstractmethod, ABC
from typing import Optional

import sys
from syllabiky.syllabiky import split_phrase
from syllabiky.DbMatcher import DbMatcher
from tools import sk, en
from tools.exception import WordSegmentException
from tools.splinter import SlovakGraphicSplinter, SlovakPhoneticSplinter, EnglishGraphicSplinter, \
    EnglishPhoneticSplinter, Overlap
from tools.corpora import SlovakExactCorpus, SlovakSubstringCorpus, EnglishExactCorpus, EnglishSubstringCorpus


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

    def __sw_phonetic(self):
        if self.__lang == 'EN' and self.TRANSCRIPTION_MANAGER is not None:
            self['G_sw_phonetic'] = self.TRANSCRIPTION_MANAGER[self['sw_graphic']]

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

    __MATCHER = DbMatcher()

    def __init__(self, table, data: dict):
        super().__init__(table, data)
        self.__lang = self['survey_language']
        if self.__lang not in ('SK', 'EN'):
            raise Exception

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

    # def __n_of_overlapping_letters(self):
    #     pass
    #
    # def __n_of_overlapping_phones(self):
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

    def __lexsh(self):

        cls = SlovakGraphicSplinter if self.__lang == 'SK' else EnglishGraphicSplinter

        lexsh_main = []
        is_lexsh_modified = False
        lexsh_whatm = []

        for i in range(4):
            sw_graphic = self['sw{}_graphic'.format(i+1)]
            gs_splinter = self['gs_sw{}_splinter'.format(i+1)]
            gm_splinter = self['gm_sw{}_splinter'.format(i+1)]
            if not sw_graphic or not gs_splinter:
                break

            strict = cls(self['nu_graphic'], sw_graphic, True)
            strict.set_splinter(gs_splinter)
            lexsh = strict.lexical_shortening
            if lexsh:
                lexsh_main.append(lexsh.name)

                if gm_splinter:

                    if gs_splinter == gm_splinter:
                        # splintre su rovnake => ziadna zmena
                        lexsh_whatm.append(lexsh_main[-1])
                    else:
                        modified = cls(self['nu_graphic'], sw_graphic, False)
                        modified.set_splinter(gm_splinter)
                        lexsh = modified.lexical_shortening
                        if lexsh:
                            is_lexsh_modified = True
                            lexsh_whatm.append(lexsh.name + 'm')

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
                splinter = self['{}s_sw{}_splinter'.format('g' if graphic else 'p', i + 1)]
                if not source_word or not splinter:
                    break

                try:
                    strict = SplinterCls(naming_unit, source_word, True)
                    strict.set_splinter(splinter)
                except WordSegmentException as e:
                    print(e, file=sys.stderr)
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

    def generate(self):
        self.__nu_syllabic()
        self.__nu_graphic_len()
        self.__nu_phonetic_len()
        self.__nu_syllabic_len()
        self.__lexsh()
        self.__overlap()


class Splinter(Entity):

    # korpusy ma nastavit volajuci
    SK_EXACT_CORPUS: Optional[SlovakExactCorpus] = None
    SK_SUBSTRING_CORPUS: Optional[SlovakSubstringCorpus] = None
    EN_EXACT_CORPUS: Optional[EnglishExactCorpus] = None
    EN_SUBSTRING_CORPUS: Optional[EnglishSubstringCorpus] = None

    def corpus_freq(self):

        # chceme to iba pre blendy
        if self['wf_process'] != 'blend':
            return

        if self['type_of_splinter'].startswith('graphic') is False:
            return

        if self['survey_language'] == 'SK' and self.SLOVAK_CORPUS is not None:
            for i in range(1, 4+1):
                spl = self[f'sw{i}_splinter']
                if not spl:
                    spl = self[f'G_sw{i}_splinter']
                self[f'sw{i}_splinter_freq_exact'] = self.SK_EXACT_CORPUS.get_frequency(spl) if spl else None
                self[f'sw{i}_splinter_freq_any'] = self.SK_SUBSTRING_CORPUS.get_frequency(spl) if spl else None

        elif self['survey_language'] == 'EN' and self.BNC_CORPUS is not None:
            for i in range(1, 4+1):
                spl = self[f'sw{i}_splinter']
                if not spl:
                    spl = self[f'G_sw{i}_splinter']
                self[f'sw{i}_splinter_freq_exact'] = self.EN_EXACT_CORPUS.get_frequency(spl) if spl else None
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
                        s = cls(nu, sw, strict)
                        if s.find_splinter():
                            splinter = s.splinter
                            length = s.length
                    except WordSegmentException:
                        pass

                    self['G_sw{}_splinter'.format(i)] = splinter
                    self['G_sw{}_splinter_len'.format(i)] = length

        self.corpus_freq()
