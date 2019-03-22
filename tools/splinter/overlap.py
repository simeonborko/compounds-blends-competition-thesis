from typing import List, Sequence

from cached_property import cached_property

from tools.splinter import Alignment


class Overlap:

    def __init__(self, naming_unit: Sequence, alignments: List[Alignment]):

        if len(naming_unit) == 0:
            raise ValueError("naming_unit cannot be an empty sequence")
        if None in alignments:
            raise ValueError("alignments cannot contain None")

        self._naming_unit = naming_unit
        self._nu_length = len(naming_unit)
        self._alignments = alignments

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
    def overlapping_segments(self) -> list:
        return [self._naming_unit[idx] for idx in self._overlapping_indexes]

    @property
    def number_of_overlapping_segments(self) -> int:
        return len(self._overlapping_indexes)
