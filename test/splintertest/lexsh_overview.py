from unittest import TestCase

from src.tools.splinter import EnglishGraphicSplinter, LexshType


class LexshTestOverview(TestCase):

    def __en(self, nu: str, sw: str, lexsh_type: LexshType):
        s = EnglishGraphicSplinter(nu, sw, True)
        self.assertTrue(s.find_splinter())
        self.assertEqual(lexsh_type, s.lexical_shortening)

    def test_rs_fsw(self):
        self.__en('crocoduck', 'crocodile', LexshType.RS)
        self.__en('crocoduck', 'duck', LexshType.FSW)

    def test_rs_ls(self):
        self.__en('elifly', 'elephant', LexshType.RS)
        self.__en('elifly', 'butterfly', LexshType.LS)
