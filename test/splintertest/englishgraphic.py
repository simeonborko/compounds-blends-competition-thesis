from unittest import TestCase

from tools.splinter import EnglishGraphicSplinter


class FindSplinter(TestCase):

    def test_0(self):
        s = EnglishGraphicSplinter('Bug', 'bunny', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('Bu', s.splinter)
        self.assertEqual(2, s.length)

    def test_1(self):
        s = EnglishGraphicSplinter('bock', 'bokk', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('bo', s.splinter)
        self.assertEqual(2, s.length)

    def test_2(self):
        s = EnglishGraphicSplinter('bock', 'bokk', True)
        self.assertTrue(s.find_splinter())
        self.assertEqual('bock', s.splinter)
        self.assertEqual(4, s.length)


class SetSplinter(TestCase):

    def test_0(self):
        s = EnglishGraphicSplinter('Bug', 'bunny', True)
        self.assertTrue(s.set_splinter('Bu'))
        self.assertEqual('Bu', s.splinter)
        self.assertEqual(2, s.length)

    def test_1(self):
        s = EnglishGraphicSplinter('bock', 'bokk', True)
        self.assertTrue(s.set_splinter('bo'))
        self.assertEqual('bo', s.splinter)
        self.assertEqual(2, s.length)

    def test_2(self):
        s = EnglishGraphicSplinter('bock', 'bokk', True)
        self.assertTrue(s.set_splinter('k'))
        self.assertEqual('k', s.splinter)
        self.assertEqual(1, s.length)

    def test_3(self):
        s = EnglishGraphicSplinter('bock', 'bokk', True)
        self.assertTrue(s.set_splinter('bock'))
        self.assertEqual('bock', s.splinter)
        self.assertEqual(4, s.length)

    def test_4(self):
        s = EnglishGraphicSplinter('bock', 'bokk', True)
        self.assertTrue(s.set_splinter('bock'))
        self.assertEqual('bock', s.splinter)
        self.assertEqual(4, s.length)



