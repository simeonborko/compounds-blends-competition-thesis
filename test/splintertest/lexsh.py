from typing import Optional
from unittest import TestCase

from src.tools.splinter import SlovakGraphicSplinter, LexshType



class LexshTest(TestCase):

    def __test(self, sw: str, splinter: str, expected: Optional[LexshType]):
        s = SlovakGraphicSplinter('123', sw, True)
        self.assertTrue(s.find_splinter())
        self.assertEqual(splinter, s.splinter)
        self.assertEqual(expected, s.lexical_shortening)

    def test_1(self):
        self.__test('01', '1', LexshType.LS)

    def test_2(self):
        self.__test('012', '12', LexshType.LS)

    def test_3(self):
        self.__test('0123', '123', LexshType.LS)

    def test_4(self):
        self.__test('01234', '123', LexshType.RSLS)

    def test_5(self):
        self.__test('1', '1', LexshType.FSW)

    def test_6(self):
        self.__test('12', '12', LexshType.FSW)

    def test_7(self):
        self.__test('123', '123', LexshType.FSW)

    def test_8(self):
        self.__test('1234', '123', LexshType.RS)

    def test_9(self):
        self.__test('2', '2', LexshType.FSW)

    def test_10(self):
        self.__test('23', '23', LexshType.FSW)

    def test_11(self):
        self.__test('234', '23', LexshType.RS)

    def test_12(self):
        self.__test('3', '3', LexshType.FSW)

    def test_13(self):
        self.__test('34', '3', LexshType.RS)
