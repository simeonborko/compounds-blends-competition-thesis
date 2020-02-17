import sys
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from typing import Optional, Sequence, List, Callable

from unidecode import unidecode

from tools import sk, en


class LexshType(Enum):
    FSW = auto()
    LS = auto()
    RS = auto()
    RSLS = auto()


def parse_lexsh_type(lexsh: str, sw_number: int) -> Optional[LexshType]:
    """
    :param lexsh: Retazec na parsovanie, jednotlive lexical shortening su oddelene +
    :param sw_number: Cislo zdrojoveho slova, zacina od 1.
    :return: LexshType alebo None
    """
    if not lexsh:
        return None
    lst = lexsh.split('+')
    if (sw_number - 1) >= len(lst):
        return None
    one_lexsh = lst[sw_number - 1]
    for enum_entry in LexshType:
        if one_lexsh == enum_entry.name:
            return enum_entry
    return None


class SplitPointType(Enum):
    NUCL_CODA = auto()   # samohlaska - spoluhlaska
    SYLLABLE = auto()
    ONSET_NUCL = auto()  # spoluhlaska - samohlaska

    def __str__(self):
        if self == SplitPointType.NUCL_CODA:
            return 'nucleus-coda'
        elif self == SplitPointType.SYLLABLE:
            return 'syllable'
        elif self == SplitPointType.ONSET_NUCL:
            return 'onset-nucleus'
        else:
            return super().__str__()


class Alignment:

    def __init__(self, nu: Sequence, sw: Sequence, nu_range: range, sw_range: range, nu_orig: Sequence):
        self._nu = nu
        self._sw = sw
        self._nu_range = nu_range
        self._sw_range = sw_range
        self._nu_orig = nu_orig
        self._score = None

    @property
    def score(self) -> int:
        """Zisti pocet rovnakych casti zo zaciatku"""
        if self._score is None:
            score = 0
            nu = self._nu[self._nu_range.start:self._nu_range.stop]
            sw = self._sw[self._sw_range.start:self._sw_range.stop]
            for pair in zip(nu, sw):
                if pair[0] == pair[1]:
                    score += 1
                else:
                    break
            self._score = score
        return self._score

    @property
    def splinter(self) -> Sequence:
        """Vrati rovnaku cast prilozenia z NAMING UNIT"""
        start = self._nu_range.start
        stop = start + self.score
        return self._nu_orig[start:stop]

    @property
    def nu_range(self) -> range:
        return self._nu_range

    @property
    def sw_range(self) -> range:
        return self._sw_range

    @property
    def nu_length(self) -> int:
        return len(self._nu)

    # @property
    # def sw_length(self) -> int:
    #     return len(self._sw)


class Splinter:

    def __init__(self, namingunit: Sequence, sourceword: Sequence, namingunit_orig: Optional[Sequence] = None):
        self.__namingunit = namingunit
        self.__sourceword = sourceword
        self.__namingunit_orig = namingunit_orig if namingunit_orig is not None else namingunit
        self.__alignment = None

        self._sourceword = sourceword  # kvoli get_split_point

    def __all_alignments(self) -> List[Alignment]:
        aligns = []
        for sw_start in range(len(self.__sourceword)):
            for nu_start in range(len(self.__namingunit)):
                for sw_stop in range(sw_start+1, len(self.__sourceword)+1):
                    for nu_stop in range(nu_start+1, len(self.__namingunit)+1):
                        aligns.append(Alignment(
                            self.__namingunit,
                            self.__sourceword,
                            range(nu_start, nu_stop),
                            range(sw_start, sw_stop),
                            self.__namingunit_orig
                        ))
        return aligns

    def find_splinter(self) -> bool:
        if self.__alignment is not None:
            raise Exception
        aligns = self.__all_alignments()
        if len(aligns) > 0:
            alignment = max(aligns, key=lambda align: align.score)
            if alignment.score > 0:
                self.__alignment = alignment
                return True
        return False

    def set_splinter(self, splinter: Sequence) -> bool:
        if self.__alignment is not None:
            raise Exception
        self.__alignment = next(filter(lambda align: align.splinter == splinter, self.__all_alignments()), None)
        return self.__alignment is not None

    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @property
    def splinter(self) -> Optional[Sequence]:
        return self.__alignment.splinter if self.__alignment is not None else None

    @property
    def length(self) -> Optional[int]:
        # nesmie sa pouzit self.splinter, pretoze self.splinter je menena v detskych triedach
        return len(self.__alignment.splinter) if self.__alignment is not None else None

    @property
    def lexical_shortening(self) -> Optional[LexshType]:

        if self.__alignment is None:
            return None

        if len(self.alignment.sw_range) == len(self.__sourceword):
            return LexshType.FSW
        elif self.alignment.sw_range.start == 0:
            return LexshType.RS
        elif self.alignment.sw_range.stop == len(self.__sourceword):
            return LexshType.LS
        else:
            return LexshType.RSLS


class StringSplinter(Splinter, metaclass=ABCMeta):

    def __init__(self, namingunit: str, sourceword: str, strict: bool, list_fn: Callable[[str], list]):
        self._list_fn = list_fn
        if strict:
            super().__init__(list_fn(namingunit), list_fn(sourceword))
        else:
            super().__init__(
                list_fn(self.modify(namingunit)),
                list_fn(self.modify(sourceword)),
                list_fn(namingunit)
            )

    @staticmethod
    @abstractmethod
    def modify(expr: str) -> str:
        raise NotImplementedError


class GraphicSplinter(StringSplinter, metaclass=ABCMeta):

    def __init__(self, namingunit: str, sourceword: str, strict: bool, list_fn: Callable[[str], list]):
        super().__init__(namingunit.lower(), sourceword.lower(), strict, list_fn)

    def set_splinter(self, splinter: str) -> bool:
        return super().set_splinter(self._list_fn(splinter))

    @property
    def splinter(self) -> Optional[str]:
        s = super().splinter
        return ''.join(s) if s else None


class PhoneticSplinter(StringSplinter, metaclass=ABCMeta):

    def set_splinter(self, splinter: str) -> bool:
        return super().set_splinter(self._list_fn(splinter.replace(' ', '')))

    @property
    def splinter(self) -> Optional[str]:
        s = super().splinter
        return ' '.join(s) if s else None


class SlovakGraphicSplinter(GraphicSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, sk.get_letters_list)

    @staticmethod
    def modify(expr: str) -> str:
        return unidecode(expr).replace('y', 'i')

    def __analyze_split_point_pair(self, sw_a_idx: int, sw_b_idx: int, map_letter_to_syll: List[int]) -> Optional[SplitPointType]:

        try:
            if map_letter_to_syll[sw_a_idx] != map_letter_to_syll[sw_b_idx]:
                # su v roznych slabikach
                return SplitPointType.SYLLABLE
        except IndexError as e:
            print('Suppressed error in __analyze_split_point_pair', map_letter_to_syll, sw_a_idx, sw_b_idx, e, file=sys.stderr)
            return None

        a_type = sk.Letters.get_type(self._sourceword[sw_a_idx])
        b_type = sk.Letters.get_type(self._sourceword[sw_b_idx])

        if a_type in ('v', 'd') and b_type == 'c':
            # samohlaska / dvojhlaska, spoluhlaska
            return SplitPointType.NUCL_CODA

        elif a_type == 'c' and b_type in ('v', 'd'):
            # spoluhlaska, samohlaska / dvojhlaska
            return SplitPointType.ONSET_NUCL

        else:
            return None

    def get_split_point(self, sw_syllabic: str) -> Optional[SplitPointType]:
        """
        syllables je string, slabiky su oddelene pomlckami (-)
        """

        if not sw_syllabic:
            return None

        # chyz-ka => 0 0 0 1 1
        # sla-bi-ky => 0 0 0 1 1 2 2
        map_letter_to_syll = sk.get_map_letter_to_syll(sw_syllabic)

        lexsh = self.lexical_shortening
        rng = self.alignment.sw_range

        if lexsh == LexshType.RS:
            return self.__analyze_split_point_pair(rng.stop - 1, rng.stop, map_letter_to_syll)

        elif lexsh == LexshType.LS:
            return self.__analyze_split_point_pair(rng.start - 1, rng.start, map_letter_to_syll)

        else:
            return None


class SlovakPhoneticSplinter(PhoneticSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, sk.get_phones_list)

    @staticmethod
    def modify(expr: str) -> str:
        return expr.replace(':', '')


class EnglishGraphicSplinter(GraphicSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, en.get_letters_list)

    @staticmethod
    def modify(expr: str) -> str:
        return unidecode(expr).replace('c', 'k')


class EnglishPhoneticSplinter(PhoneticSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, en.get_phones_list)

    @staticmethod
    def modify(expr: str) -> str:
        return en.Phones.shorten_vowels(expr)

    def __analyze_split_point_pair(self, sw_a_idx: int, sw_b_idx: int, map_letter_to_syll: List[int]) -> Optional[SplitPointType]:

        if map_letter_to_syll[sw_a_idx] != map_letter_to_syll[sw_b_idx]:
            # su v roznych slabikach
            return SplitPointType.SYLLABLE

        a_type = en.Phones.get_type(self._sourceword[sw_a_idx])
        b_type = en.Phones.get_type(self._sourceword[sw_b_idx])

        if a_type in ('v', 'd') and b_type == 'c':
            # samohlaska / dvojhlaska, spoluhlaska
            return SplitPointType.NUCL_CODA

        elif a_type == 'c' and b_type in ('v', 'd'):
            # spoluhlaska, samohlaska / dvojhlaska
            return SplitPointType.ONSET_NUCL

        else:
            return None

    def get_split_point(self, sw_phonetic: str) -> Optional[SplitPointType]:

        if not sw_phonetic:
            return None

        map_phone_to_syll = en.get_map_phone_to_syll(sw_phonetic)

        lexsh = self.lexical_shortening
        rng = self.alignment.sw_range

        if lexsh == LexshType.RS:
            return self.__analyze_split_point_pair(rng.stop - 1, rng.stop, map_phone_to_syll)

        elif lexsh == LexshType.LS:
            return self.__analyze_split_point_pair(rng.start - 1, rng.start, map_phone_to_syll)

        else:
            return None
