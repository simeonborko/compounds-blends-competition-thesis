from syllabiky.syllabiky import split_phrase
from syllabiky.DbMatcher import DbMatcher
from tools import sk, en
from Entity import Entity


class SourceWord(Entity):

    CORPUS = None  # corpus ma nastavit volajuci
    _ALLOWED = ('frequency_in_snc',)  # ktore stlpce je povolene zmenit bez toho, aby zacinali G_
    _PRIMARY = ('sw_graphic', 'first_language', 'survey_language')  # nezmenitelne stlpce
    __MATCHER = DbMatcher()

    def __init__(self, data: dict):
        super().__init__(data)
        self.__lang = self['survey_language']

    def sw_syllabic(self):
        if self.__lang == 'SK':
            self['G_sw_syllabic'] = split_phrase(self['sw_graphic'], self.__MATCHER)

    def sw_graphic_len(self):
        if self.__lang == 'SK':
            self['G_sw_graphic_len'] = sk.count_letters(self['sw_graphic'])
        elif self.__lang == 'EN':
            self['G_sw_graphic_len'] = en.count_letters(self['sw_graphic'])

    def sw_phonetic_len(self):
        if self.__lang == 'SK':
            self['G_sw_phonetic_len'] = sk.count_phones(self['sw_phonetic'])
        elif self.__lang == 'EN':
            self['G_sw_phonetic_len'] = en.count_phones(self['sw_phonetic'])

    def sw_syllabic_len(self):
        self.sw_syllabic()
        if self.__lang == 'SK':
            self['G_sw_syllabic_len'] = self['G_sw_syllabic'].count('-') + 1
        elif self.__lang == 'EN':
            self['G_sw_syllabic_len'] = en.count_syllables(self['sw_phonetic'])

    def frequency_in_snc(self):
        if self.__lang == 'SK':
            self['frequency_in_snc'] = self.CORPUS.get_frequency(self['sw_graphic'])
