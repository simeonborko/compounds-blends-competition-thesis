from unittest import TestCase

from tools.splinter import Splinter


class FindSplinter(TestCase):

    def test_0(self):
        s = Splinter('krokacka', 'krokodil')
        self.assertTrue(s.find_splinter())
        self.assertEqual('krok', s.splinter)

    def test_1(self):
        s = Splinter('skunkey', 'monkey')
        self.assertTrue(s.find_splinter())
        self.assertEqual('nkey', s.splinter)

    def test_2(self):
        s = Splinter('abcdefg', 'bce')
        self.assertTrue(s.find_splinter())
        self.assertEqual('bc', s.splinter)

    def test_3(self):
        s = Splinter(['k', 'æ', 'm', 'p', 't', 'æ', 'ŋ', 'k'], ['k', 'æ', 'm', 'p', 'ə', 'r'])
        self.assertTrue(s.find_splinter())
        self.assertEqual(['k', 'æ', 'm', 'p'], s.splinter)


class SetSplinter(TestCase):

    def test_0(self):
        s = Splinter('krokacka', 'krokodil')
        self.assertTrue(s.set_splinter('krok'))
        self.assertEqual('krok', s.splinter)

    def test_1(self):
        s = Splinter('krokacka', 'krokodil')
        self.assertTrue(s.set_splinter('rok'))
        self.assertEqual('rok', s.splinter)

    def test_2(self):
        s = Splinter('abcdefg', 'bcef')
        self.assertTrue(s.set_splinter('bc'))
        self.assertEqual('bc', s.splinter)
        self.assertRaises(Exception, s.find_splinter)
        self.assertRaises(Exception, s.set_splinter)

    def test_3(self):
        s = Splinter('abcdefg', 'bcef')
        self.assertTrue(s.set_splinter('ef'))
        self.assertEqual('ef', s.splinter)
        self.assertRaises(Exception, s.find_splinter)
        self.assertRaises(Exception, s.set_splinter)

    def test_4(self):
        s = Splinter(['k', 'æ', 'm', 'p', 't', 'æ', 'ŋ', 'k'], ['k', 'æ', 'm', 'p', 'ə', 'r'])
        self.assertTrue(s.set_splinter(['k', 'æ', 'm', 'p']))
        self.assertEqual(['k', 'æ', 'm', 'p'], s.splinter)

    def test_5(self):
        s = Splinter('krokacka', 'krokodil')
        self.assertFalse(s.set_splinter('chyba'))
        self.assertIsNone(s.splinter)
