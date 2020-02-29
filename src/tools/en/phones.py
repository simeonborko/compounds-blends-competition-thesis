from typing import List

import itertools

from .syllables import remove_syllable_division, get_syllables
import re
import sys

# https://dictionary.cambridge.org/help/phonetics.html


class Phones:
    LONG = ('iː', 'ɑː', 'uː', 'ɔː', 'ɜː')
    SHORT = ('ɪ', 'æ', 'ʊ', 'ɒ', 'ʌ', 'e', 'ə', 'ɚ', 'ɝ')
    VOICED = ('b', 'd', 'g', 'ɡ', 'v', 'ð', 'z', 'ʒ', 'dʒ', 'l', 'r', 'j', 'w', 'm', 'n', 'ŋ')
    VOICELESS = ('p', 't', 'k', 'f', 'θ', 's', 'ʃ', 'tʃ')
    DIPHTHONGS = ('eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'əʊ', 'oʊ', 'ɪə', 'eə', 'ʊə')
    OTHER = ('h', 'i', 'u')
    ALL = LONG + SHORT + VOICED + VOICELESS + DIPHTHONGS + OTHER
    PATTERN = re.compile('|'.join(sorted(ALL, key=lambda x: len(x), reverse=True)))

    @classmethod
    def get_type(cls, phone: str) -> str:
        """Zisti typ hlasky"""
        if phone in cls.LONG or phone in cls.SHORT:
            return 'v'  # vowel
        elif phone in cls.VOICED or phone in cls.VOICELESS:
            return 'c'  # consonant
        elif phone in cls.DIPHTHONGS:
            return 'd'  # diphthong
        elif phone in cls.OTHER:
            return 'o'  # other

    @staticmethod
    def shorten_vowels(expr: str) -> str:
        return expr.replace('iː', 'ɪ').replace('ɑː', 'ʌ').replace('uː', 'ʊ')


def get_phones_list(phonetic, query='', number=None):
    """
    Vytvori zoznam hlasok. Pripadne nezname hlasky oznami na stderr.
    :param phonetic: Retazec (moze obsahovat medzery).
    :param query: Povodny retazec (pismena, nie hlasky).
    :param number: Cislo riadka vo vstupe.
    :return: Zoznam hlasok.
    """

    expr = ''.join(remove_syllable_division(phonetic))
    phones_list = Phones.PATTERN.findall(expr)

    # if sum([len(phone) for phone in phones_list]) != len(expr):
    #     found_phones = ' '.join(phones_list)
    #     print(number, query, phonetic.replace('\n', '\\n'), expr.replace('\n', '\\n'), found_phones, sep='\t',
    #           file=sys.stderr)

    return phones_list


def count_phones(phonetic, query='', number=None):
    return len(get_phones_list(phonetic, query, number))


def get_syllable_list(phonetic):
    """Ziska zoznam slabik, pricom slabika je zoznam hlasok"""
    return [get_phones_list(syllable) for syllable in get_syllables(phonetic)]


def get_syllable_lengths(phonetic):
    """Ziska pocty hlasok v slabikach"""
    return [len(syllable) for syllable in get_syllable_list(phonetic)]


def get_map_phone_to_syll(phonetic: str) -> List[int]:
    return list(itertools.chain.from_iterable(
        [i] * syll_len for i, syll_len in enumerate(get_syllable_lengths(phonetic))
    ))
