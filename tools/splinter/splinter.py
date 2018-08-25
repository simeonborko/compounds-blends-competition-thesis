from typing import Optional, Sequence, List


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
