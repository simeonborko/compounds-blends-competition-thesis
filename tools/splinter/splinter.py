from abc import ABCMeta, abstractmethod
from typing import Optional, Sequence, List, Callable

from unidecode import unidecode

from tools import sk, en


class Alignment:

    def __init__(self, nu: Sequence, sw: Sequence, nu_idx: int, sw_idx: int, nu_orig: Sequence):
        self._nu = nu
        self._sw = sw
        self._nu_idx = nu_idx
        self._sw_idx = sw_idx
        self._nu_orig = nu_orig
        self._score = None

    @property
    def score(self) -> int:
        """Zisti pocet rovnakych casti zo zaciatku"""
        if self._score is None:
            score = 0
            for pair in zip(self._nu[self._nu_idx:], self._sw[self._sw_idx:]):
                if pair[0] == pair[1]:
                    score += 1
                else:
                    break
            self._score = score
        return self._score

    @property
    def splinter(self) -> Sequence:
        """Vrati rovnaku cast prilozenia z NAMING UNIT"""
        start = self._nu_idx
        stop = start + self.score
        return self._nu_orig[start:stop]


class Splinter:

    def __init__(self, namingunit: Sequence, sourceword: Sequence, namingunit_orig: Optional[Sequence] = None):
        self.__namingunit = namingunit
        self.__sourceword = sourceword
        self.__namingunit_orig = namingunit_orig if namingunit_orig is not None else namingunit
        self.__alignment = None

    def __all_alignments(self) -> List[Alignment]:
        aligns = []
        for sw_idx in range(len(self.__sourceword)):
            for nu_idx in range(len(self.__namingunit)):
                aligns.append(Alignment(self.__namingunit, self.__sourceword, nu_idx, sw_idx, self.__namingunit_orig))
        return aligns

    def find_splinter(self) -> bool:
        if self.__alignment is not None:
            raise Exception
        alignment = max(self.__all_alignments(), key=lambda align: align.score)
        if alignment.score > 0:
            self.__alignment = alignment
            return True
        else:
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


class SlovakGraphicSplinter(StringSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, sk.get_letters_list)

    @staticmethod
    def modify(expr: str) -> str:
        return unidecode(expr).replace('y', 'i')


class SlovakPhoneticSplinter(StringSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, sk.get_phones_list)

    @staticmethod
    def modify(expr: str) -> str:
        return expr.replace(':', '')


class EnglishGraphicSplinter(StringSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, en.get_letters_list)

    @staticmethod
    def modify(expr: str) -> str:
        return unidecode(expr).replace('c', 'k')


class EnglishPhoneticSplinter(StringSplinter):

    def __init__(self, namingunit: str, sourceword: str, strict: bool):
        super().__init__(namingunit, sourceword, strict, en.get_phones_list)

    @staticmethod
    def modify(expr: str) -> str:
        return en.Phones.shorten_vowels(expr)