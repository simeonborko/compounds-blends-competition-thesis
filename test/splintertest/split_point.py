from unittest import TestCase

from tools.splinter import SlovakGraphicSplinter, LexshType, SplitPointType, EnglishPhoneticSplinter


class SplitPointTest(TestCase):

    def test_sk(self):
        s = SlovakGraphicSplinter('krokačka', 'krokodíl', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('krok', s.splinter)
        self.assertEqual(LexshType.RS, s.lexical_shortening)
        self.assertEqual(
            SplitPointType.ONSET_NUCL,
            s.get_split_point('kro-kač-ka'),
        )

    def __test_en(self, nu_phonetic, sw_phonetic, ex_splinter, ex_lexsh, ex_split_point):
        s = EnglishPhoneticSplinter(nu_phonetic, 'ˈæl.ɪ.ɡeɪ.tər', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('æ l ɪ ɡ', s.splinter)
        self.assertEqual(LexshType.RS, s.lexical_shortening)
        self.assertEqual(
            SplitPointType.ONSET_NUCL,
            s.get_split_point('ˈæl.ɪ.ɡwɪn')
        )

    def test_en_1(self):
        s = EnglishPhoneticSplinter('ˈæl.ɪ.ɡwɪn', 'ˈæl.ɪ.ɡeɪ.tər', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('æ l ɪ ɡ', s.splinter)
        self.assertEqual(LexshType.RS, s.lexical_shortening)
        self.assertEqual(
            SplitPointType.ONSET_NUCL,
            s.get_split_point('ˈæl.ɪ.ɡwɪn')
        )
    'dʒɪˈruːs'
