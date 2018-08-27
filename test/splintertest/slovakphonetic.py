from unittest import TestCase

from tools.splinter import SlovakPhoneticSplinter


class FindSplinter(TestCase):

    def test_0(self):
        s = SlovakPhoneticSplinter('alɪgɪtsa', 'alɪga:tOr', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('a l I g', s.splinter)
        self.assertEqual(4, s.length)

    def test_1(self):
        s = SlovakPhoneticSplinter('bUldOzajats', 'bUldOg', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('b U l d O', s.splinter)
        self.assertEqual(5, s.length)

    def test_2(self):
        s = SlovakPhoneticSplinter('bUldOzajats', 'zajats', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('z a j a ts', s.splinter)
        self.assertEqual(5, s.length)

    def test_3(self):
        s = SlovakPhoneticSplinter('xObOtɪ:L', 'xObOtɪ:L', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('x O b O t I: L', s.splinter)
        self.assertEqual(7, s.length)

    def test_4(self):
        s = SlovakPhoneticSplinter('xObOtɪ:L', 'xObOtɪL', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('x O b O t', s.splinter)
        self.assertEqual(5, s.length)

    def test_5(self):
        s = SlovakPhoneticSplinter('xObOtɪ:L', 'xObOtɪL', False)
        self.assertTrue(s.find_splinter())
        self.assertEqual('x O b O t I: L', s.splinter)
        self.assertEqual(7, s.length)


class SetSplinter(TestCase):

    def test_0(self):
        s = SlovakPhoneticSplinter('xObOtɪ:L', 'xObOtɪL', False)
        self.assertTrue(s.set_splinter('x O b O t I: L'))
        self.assertEqual('x O b O t I: L', s.splinter)
        self.assertEqual(7, s.length)

    def test_1(self):
        s = SlovakPhoneticSplinter('xObOtɪ:L', 'xObOtɪL', False)
        self.assertTrue(s.set_splinter('b O t ɪ:'))
        self.assertEqual('b O t I:', s.splinter)
        self.assertEqual(4, s.length)

