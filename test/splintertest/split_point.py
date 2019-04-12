from unittest import TestCase

from tools.splinter import SlovakGraphicSplinter, LexshType, SplitPointType


class SplitPointTest(TestCase):

    def test_1(self):
        s = SlovakGraphicSplinter('krokacka', 'krokodil', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('krok', s.splinter)
        self.assertEqual(LexshType.RS, s.lexical_shortening)
        self.assertEqual(
            SplitPointType.ONSET_NUCL,
            s.get_split_point('kro-kac-ka'),
        )
