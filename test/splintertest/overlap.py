from unittest import TestCase

from src.tools.splinter import Overlap, Splinter, SlovakGraphicSplinter


class OverlapTest(TestCase):

    def _krokacka(self, SplinterCls, *args):

        s1 = SplinterCls('krokačka', 'krokodíl', *args)
        s2 = SplinterCls('krokačka', 'kačka', *args)

        s1.find_splinter()
        s2.find_splinter()

        overlap = Overlap('krokačka', [s1.alignment, s2.alignment], SplinterCls)
        self.assertEqual(1, overlap.number_of_overlapping_segments)
        self.assertEqual('k', overlap.overlapping_segments)
        self.assertListEqual([3], overlap._overlapping_indexes)

    def test_krokacka(self):
        self._krokacka(Splinter)

    def test_krokacka_strict(self):
        self._krokacka(SlovakGraphicSplinter, True)

    def test_krokacka_nonstrict(self):
        self._krokacka(SlovakGraphicSplinter, False)

    def _no_overlap(self, nu, sw1, sw2):

        s1 = Splinter(nu, sw1)
        s2 = Splinter(nu, sw2)

        s1.find_splinter()
        s2.find_splinter()

        overlap = Overlap(nu, [s1.alignment, s2.alignment], Splinter)
        self.assertEqual(0, overlap.number_of_overlapping_segments)
        self.assertEqual('', overlap.overlapping_segments)
        self.assertListEqual([], overlap._overlapping_indexes)

    def test_no_overlap_1(self):
        self._no_overlap('abcdef', 'abc', 'def')

    def test_no_overlap_2(self):
        self._no_overlap('abcdef', 'ab', 'def')
