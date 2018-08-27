from unittest import TestCase

from tools.splinter import SlovakGraphicSplinter


class FindSplinter(TestCase):

    def test_0(self):
        s = SlovakGraphicSplinter('krokacka', 'krokodil', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('krok', s.splinter)

    def test_1(self):
        s = SlovakGraphicSplinter('skunkey', 'monkey', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('nkey', s.splinter)
        self.assertEqual(4, s.length)

    def test_2(self):
        s = SlovakGraphicSplinter('abcdefg', 'bce', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('bc', s.splinter)

    def test_3(self):
        s = SlovakGraphicSplinter('abčdef', 'abč', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('abč', s.splinter)

    def test_4(self):
        s = SlovakGraphicSplinter('abčdef', 'abc', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('ab', s.splinter)

    def test_5(self):
        s = SlovakGraphicSplinter('abčdef', 'abc', False)
        self.assertTrue(s.find_splinter())
        self.assertEqual('abč', s.splinter)
        self.assertEqual(3, s.length)

    def test_6(self):
        s = SlovakGraphicSplinter('vtipy', 'vtipi', False)
        self.assertTrue(s.find_splinter())
        self.assertEqual('vtipy', s.splinter)
        self.assertEqual(5, s.length)


class SetSplinter(TestCase):
    def test_0(self):
        s = SlovakGraphicSplinter('krokacka', 'krokodil', True)
        self.assertTrue(s.set_splinter('krok'))
        self.assertEqual('krok', s.splinter)

    def test_1(self):
        s = SlovakGraphicSplinter('krokacka', 'krokodil', False)
        self.assertTrue(s.set_splinter('rok'))
        self.assertEqual('rok', s.splinter)
