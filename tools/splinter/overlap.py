from typing import List

from cached_property import cached_property

from tools.splinter import Alignment


class Overlap:

    def __init__(self, naming_unit: str, alignments: List[Alignment], space: bool = False):
        """
        :param naming_unit: naming unit, pre ktore sa bude robit overlap
        :param alignments: zarovnania s jednotlivymi zdrojovymi slovami
        :param space: ci vo vystupnom retazci vkladat medzery medzi jednotlive segmenty
        """

        if len(naming_unit) == 0:
            raise ValueError("naming_unit cannot be an empty sequence")
        if len(alignments) == 0:
            raise ValueError("alignments cannot be empty")
        if None in alignments:
            raise ValueError("alignments cannot contain None")

        nu_lengths = {a.nu_length for a in alignments}
        if len(nu_lengths) != 1:
            raise ValueError("aligments have to be based on one and the same naming unit")

        self._naming_unit = naming_unit
        self._nu_length = next(iter(nu_lengths))
        self._alignments = alignments
        self._space = space

    def _counters(self) -> List[int]:

        for align in self._alignments:
            if align.nu_length != self._nu_length:
                raise ValueError(f"self._nu_length ({self._nu_length}) does not match align.nu_length ({align.nu_length})")

        counters = [0] * self._nu_length
        for align in self._alignments:
            for i in align.nu_range:
                counters[i] += 1

        return counters

    @cached_property
    def _overlapping_indexes(self) -> List[int]:
        return [idx for idx, counter in enumerate(self._counters()) if counter > 1]

    @property
    def overlapping_segments(self) -> str:
        segments = [self._naming_unit[idx] for idx in self._overlapping_indexes]
        return (' ' if self._space else '').join(segments)

    @property
    def number_of_overlapping_segments(self) -> int:
        return len(self._overlapping_indexes)
