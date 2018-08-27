from unittest import TestCase

from tools.splinter import EnglishPhoneticSplinter


class FindSplinter(TestCase):

    def test_0(self):
        s = EnglishPhoneticSplinter('ˈiː.ɡ.lən', 'ˈlaɪ.ən', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('ə n', s.splinter)
        self.assertEqual(2, s.length)

    def test_1(self):
        s = EnglishPhoneticSplinter('ɜːθ sek.ənd', 'ˈsek.ənd', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('s e k ə n d', s.splinter)
        self.assertEqual(6, s.length)

    def test_2(self):
        s = EnglishPhoneticSplinter('ˈiː.ɡər', 'ˈtɪ.ɡər', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('ɡ ə r', s.splinter)
        self.assertEqual(3, s.length)

    def test_3(self):
        s = EnglishPhoneticSplinter('ˈiː.ɡər', 'ˈtɪ.ɡər', False)
        self.assertTrue(s.find_splinter())
        self.assertEqual('iː ɡ ə r', s.splinter)
        self.assertEqual(4, s.length)


class SetSplinter(TestCase):

    def test_0(self):
        s = EnglishPhoneticSplinter('ˈiː.ɡ.lən', 'ˈlaɪ.ən', True)
        self.assertTrue(s.set_splinter('ə n'))
        self.assertEqual('ə n', s.splinter)
        self.assertEqual(2, s.length)

    def test_1(self):
        s = EnglishPhoneticSplinter('ɜːθ sek.ənd', 'ˈsek.ənd', True)
        self.assertTrue(s.set_splinter('s e k ə n d'))
        self.assertEqual('s e k ə n d', s.splinter)
        self.assertEqual(6, s.length)

    def test_1b(self):
        s = EnglishPhoneticSplinter('ɜːθ sek.ənd', 'ˈsek.ənd', True)
        self.assertTrue(s.set_splinter('k ə n'))
        self.assertEqual('k ə n', s.splinter)
        self.assertEqual(3, s.length)

    def test_2(self):
        s = EnglishPhoneticSplinter('ˈiː.ɡər', 'ˈtaɪ.ɡər', True)
        self.assertTrue(s.set_splinter('ɡ ə r'))
        self.assertEqual('ɡ ə r', s.splinter)
        self.assertEqual(3, s.length)

    def test_3(self):
        s = EnglishPhoneticSplinter('ˈiː.ɡər', 'ˈtɪ.ɡər', False)
        self.assertTrue(s.set_splinter('iː ɡ ə r'))
        self.assertEqual('iː ɡ ə r', s.splinter)
        self.assertEqual(4, s.length)
