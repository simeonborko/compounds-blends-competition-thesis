from typing import Type, Union
from unittest import TestCase

from src.tools.splinter import EnglishGraphicSplinter, SlovakGraphicSplinter, LexshType


class LexshTestOverview(TestCase):

    def __test(self, cls: Union[Type[EnglishGraphicSplinter], Type[SlovakGraphicSplinter]],
               nu: str, sw: str, lexsh_type: LexshType):
        s = cls(nu, sw, True)
        self.assertTrue(s.find_splinter())
        self.assertEqual(lexsh_type, s.lexical_shortening)

    def __en(self, nu: str, sw: str, lexsh_type: LexshType):
        self.__test(EnglishGraphicSplinter, nu, sw, lexsh_type)

    def __sk(self, nu: str, sw: str, lexsh_type: LexshType):
        self.__test(SlovakGraphicSplinter, nu, sw, lexsh_type)

    def test_rs_fsw(self):
        self.__en('crocoduck', 'crocodile', LexshType.RS)
        self.__en('crocoduck', 'duck', LexshType.FSW)

    def test_rs_ls(self):
        self.__en('elifly', 'elephant', LexshType.RS)
        self.__en('elifly', 'butterfly', LexshType.LS)

    def test_rs_ls_upcase(self):
        self.__en('Elifly', 'elephant', LexshType.RS)
        self.__en('Elifly', 'butterfly', LexshType.LS)
