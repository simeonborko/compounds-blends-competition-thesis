from abc import ABC, abstractmethod
from unidecode import unidecode

from .interface import get_interfaces
from .letters import count_letters
from .phones import get_phones_list, get_syllable_lengths, Phones
from .syllables import count_syllables, get_syllables
from typing import Union


class Splinter(ABC):
    """Po vytvoreni objektu sa ma pouzit metoda find"""

    def __init__(self, nu: str, sw: str, len_fn=len):
        self.orig_nu = self.nu = nu.strip()
        self.sw = sw.strip()
        self.len_fn = len_fn
        self.alignment = None

    def find(self) -> bool:
        """Najde alignment. Vracia bool ci nasiel."""
        alignments = []
        for sw_idx in range(len(self.sw)):
            for nu_idx in range(len(self.nu)):
                alignments.append(Alignment(self.nu, self.sw, nu_idx, sw_idx, self.orig_nu))
        alignment = max(alignments, key=lambda align: align.score)
        if alignment.score > 0:
            self.alignment = alignment
            return True
        return False

    @abstractmethod
    def get_str(self) -> str: pass

    @abstractmethod
    def get_length(self) -> int: pass

    def get_sw_ratio(self) -> float:
        return self.get_length() / self.len_fn(self.sw)

    def get_nu_ratio(self) -> float:
        return self.get_length() / self.len_fn(self.nu)


class GraphicSplinter(Splinter):

    def __init__(self, nu, sw):
        super().__init__(nu, sw, count_letters)
        self.nu = self.nu.lower()
        self.sw = self.sw.lower()

    def get_str(self):
        return self.alignment.generate()

    def get_length(self):
        return count_letters(self.get_str())


class SoftGraphicSplinter(GraphicSplinter):

    def __init__(self, nu, sw):
        super().__init__(nu, sw)
        self.nu = unidecode(self.nu).replace('c', 'k')
        self.sw = unidecode(self.sw).replace('c', 'k')


class PhoneticSplinter(Splinter):

    def __init__(self, nu, sw):
        super().__init__(nu, sw)  # funkciou na pocitanie dlzky je len, pretoze pocitame velkost zoznamu
        self.orig_nu = self.nu = get_phones_list(self.nu)
        self.sw_str = self.sw
        self.sw = get_phones_list(self.sw)

    def get_str(self):
        return ' '.join(self.alignment.generate())

    def get_length(self):
        return len(self.alignment.generate())

    def get_shortening_and_split_point(self):
        """Vrati shortening_type, split_point_placement. Obe mozu byt None."""

        def get_shortening_type():
            """Vrati Type of Lexical Shortening alebo None."""
            if self.len_fn(self.sw) == self.get_length():  # self.len_fn je obycajne len
                return 'FSW'
            elif self.alignment.sw_idx == 0:
                return 'RS'
            elif self.alignment.sw_idx + len(self.alignment.generate()) == len(self.sw):
                return 'LS'

        shortening = get_shortening_type()

        if shortening not in ('RS', 'LS'):
            return shortening, None

        split_interface = {
            'RS': (self.alignment.score - 1, self.alignment.score),
            'LS': (self.alignment.sw_idx - 1, self.alignment.sw_idx)
        }[shortening]

        # ohodnotit rozhranie
        # ci je slabikove
        if split_interface in get_interfaces(self.sw_str):
            return shortening, 'syllable'

        types = [Phones.get_type(self.sw[idx]) for idx in split_interface]

        if types == ['c', 'v']:
            return shortening, 'onset-nucleus'  # consonant - vowel
        elif types == ['v', 'c']:
            return shortening, 'nucleus-coda'  # vowel - consonant
        else:
            return shortening, None


class SoftPhoneticSplinter(PhoneticSplinter):

    def __init__(self, nu, sw):
        super().__init__(nu, sw)
        # TODO zmena dlhych hlasok na kratke


class SyllabicSplinter(Splinter):

    class SPP:
        s = 'syllable'
        cv = 'onset-nucleus'  # consonant - vowel
        vc = 'nucleus-coda'  # vowel - consonant

    def __init__(self, nu: str, sw: str):
        super().__init__(nu, sw)
        self.orig_nu = self.nu = get_syllables(self.orig_nu)
        self.sw = get_syllables(self.sw)

    def __get_syllables(self):
        """Na zaklade fonetickeho splintra a poctov slabik v SW vytvori zoznam slabik v splintri."""
        lengths = get_syllable_lengths(self.sw)  # pocty slabik v SW
        assert sum(lengths) == len(get_phones_list(self.sw))
        phones_list = self.alignment.generate()  # zoznam hlasok splintra
        length = 0  # pociatocna hodnota, aby sa urobil pop

        for i in range(self.alignment.sw_idx):  # odstranenie prefixu
            if length == 0:  # sme na rozhrani slabiky
                length = lengths.pop(0)  # vybratie dalsej velkosti slabiky
            length -= 1

        if length > 0:  # split point je vnutri slabiky
            self.incomplete_left = True
            lengths.insert(0, length)

        for length in lengths:
            if len(phones_list) == 0:  #
                break

            if length > len(phones_list):  # ak nemame dostatok hlasok, split point je vnutri slabiky
                minimum = len(phones_list)
                self.incomplete_right = True
            else:
                minimum = length

            self.syllables.append(phones_list[:minimum])
            phones_list = phones_list[minimum:]

    def get_str(self):
        return '.'.join(self.alignment.generate())

    def get_length(self):
        return len(self.alignment.generate())


class Alignment:
    """Trieda reprezentujuca jedno prilozenie"""

    def __init__(self, nu, sw, nu_idx, sw_idx, orig_nu):
        self.nu = nu
        self.sw = sw
        self.nu_idx = nu_idx
        self.sw_idx = sw_idx
        self.orig_nu = orig_nu
        self.score = 0
        self.__get_score()

    def __get_score(self):
        """Zisti pocet rovnakych casti zo zaciatku"""
        for pair in zip(self.nu[self.nu_idx:], self.sw[self.sw_idx:]):
            if pair[0] == pair[1]:
                self.score += 1
            else:
                break

    def generate(self):
        """Vrati rovnaku cast prilozenia"""
        start = self.nu_idx
        stop = start + self.score
        return self.orig_nu[start:stop]

    def get_segment_range(self) -> range:
        return range(self.nu_idx, self.nu_idx + self.score)


class SegmentCounter:

    def __init__(self, splinters: list):
        self.segs = [0] * len(splinters[0].nu)
        for s in splinters:
            if s.alignment:
                for i in s.alignment.get_segment_range():
                    self.segs[i] += 1

    def overlap_number(self) -> int:
        return sum(x > 1 for x in self.segs)
