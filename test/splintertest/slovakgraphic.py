from unittest import TestCase

from src.tools.splinter import SlovakGraphicSplinter


kwargs = {
    'nu_src_lang_sk': True
}


class FindSplinter(TestCase):

    def test_0(self):
        s = SlovakGraphicSplinter('krokacka', 'krokodil', True, **kwargs)
        self.assertTrue(s.find_splinter())
        self.assertEqual('krok', s.splinter)

    def test_1(self):
        s = SlovakGraphicSplinter('skunkey', 'monkey', True, **kwargs)
        self.assertTrue(s.find_splinter())
        self.assertEqual('nkey', s.splinter)
        self.assertEqual(4, s.length)

    def test_2(self):
        s = SlovakGraphicSplinter('abcdefg', 'bce', True, **kwargs)
        self.assertTrue(s.find_splinter())
        self.assertEqual('bc', s.splinter)

    def test_3(self):
        s = SlovakGraphicSplinter('abčdef', 'abč', True, **kwargs)
        self.assertTrue(s.find_splinter())
        self.assertEqual('abč', s.splinter)

    def test_4(self):
        s = SlovakGraphicSplinter('abčdef', 'abc', True, **kwargs)
        self.assertTrue(s.find_splinter())
        self.assertEqual('ab', s.splinter)

    def test_5(self):
        s = SlovakGraphicSplinter('abčdef', 'abc', False, **kwargs)
        self.assertTrue(s.find_splinter())
        self.assertEqual('abč', s.splinter)
        self.assertEqual(3, s.length)

    def test_6(self):
        s = SlovakGraphicSplinter('vtipy', 'vtipi', False, **kwargs)
        self.assertTrue(s.find_splinter())
        self.assertEqual('vtipy', s.splinter)
        self.assertEqual(5, s.length)

    def test_zaba(self):
        s = SlovakGraphicSplinter('zeba', 'žaba', True, **kwargs)
        self.assertTrue(s.find_splinter(sw_last=True))
        self.assertEqual('ba', s.splinter)
        self.assertEqual(2, s.length)


class SetSplinter(TestCase):
    def test_0(self):
        s = SlovakGraphicSplinter('krokacka', 'krokodil', True, **kwargs)
        self.assertTrue(s.set_splinter('krok'))
        self.assertEqual('krok', s.splinter)

    def test_1(self):
        s = SlovakGraphicSplinter('krokacka', 'krokodil', False, **kwargs)
        self.assertTrue(s.set_splinter('rok'))
        self.assertEqual('rok', s.splinter)
