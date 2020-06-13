from typing import Optional, List

import itertools

from src.tools.exception import WordSegmentException
from src.tools.redundant import REDUNDANT
from .phones import PHONES_PATTERN, PHONES_PATTERN_EXCLUDING_DZDZ


def replace_i(word):
    """Nahradi foneticke i spravnym symbolom"""
    return word.replace('ɪ', 'I')


def remove_redundant(word):
    """Odstrani symboly, ktore robia problemy pri pocitani"""
    word = word.strip()
    for r in REDUNDANT:
        word = word.replace(r, '')
    return word


def decapitalize(phrase):
    """Zmeni prve znaky kazdeho slova na maly znak"""
    src = phrase.split(' ')
    words = []
    for word in src:
        if word:
            word = word[0].lower() + word[1:]
        words.append(word)
    return ' '.join(words)


def get_letters_list(word, chdzdz) -> list:

    word = remove_redundant(word.lower())

    if not chdzdz:
        return list(word)

    letters = []
    for ltr in word:
        if len(letters) > 0 and (letters[-1] == 'c' and ltr == 'h' or letters[-1] == 'd' and ltr in ('z', 'ž')):
            letters[-1] += ltr
        else:
            letters.append(ltr)
    return letters


def count_letters(word, chdzdz: bool) -> int:
    """Spocita pocet pismen"""
    return len(get_letters_list(word, chdzdz))


def get_syllables_list(syllabic_form: str, chdzdz: bool) -> List[List[str]]:
    """syllabic_form je string, kde su slabiky oddelene pomlckami (-)"""
    return [
        get_letters_list(syll, chdzdz)
        for syll in syllabic_form.split('-')
    ]


def get_map_letter_to_syll(syllabic_form: str, chdzdz: bool) -> List[int]:
    """
    syllabic_form je string, kde su slabiky oddelene pomlckami (-)
    Vrati zoznam, kde na i-tej pozicii je cislo slabiky, do ktorej patri i-te pismenko.
    """
    syll_list = get_syllables_list(syllabic_form, chdzdz)
    return list(itertools.chain.from_iterable(
        [i] * len(syll) for i, syll in enumerate(syll_list)
    ))


def __find_phones(word, dzdz) -> Optional[List[str]]:
    pattern = PHONES_PATTERN if dzdz else PHONES_PATTERN_EXCLUDING_DZDZ
    phones = pattern.findall(word)
    return phones if sum(len(phone) for phone in phones) == len(word) else None


def get_phones_list(word, dzdz, rep_i=True) -> List[str]:
    """Ziska zoznam fonem"""

    if rep_i:
        word = replace_i(word)
    word = remove_redundant(word)

    phones = __find_phones(word, dzdz)
    if phones:
        return phones

    phones_decap = __find_phones(decapitalize(word), dzdz)
    if phones_decap:
        return phones_decap

    raise WordSegmentException(word, phones)


def count_phones(word, dzdz, rep_i=True):
    """Count phones in word in phonetic transcription."""
    return len(get_phones_list(word, dzdz, rep_i))
