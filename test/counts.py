from unittest import TestCase

from src.tools import en
from src.tools import sk
from src.tools.exception import WordSegmentException


class SK(TestCase):

    def test_letters(self):
        self.assertEqual(5, sk.count_letters('Betka', True))
        self.assertEqual(9, sk.count_letters('dekorácia', True))
        self.assertEqual(4, sk.count_letters('dziňa', True))
        self.assertEqual(5, sk.count_letters('dziňa', False))
        self.assertEqual(3, sk.count_letters('džús', True))
        self.assertEqual(9, sk.count_letters('Alice Rock', True))

    def test_phones(self):
        self.assertEqual(8, sk.count_phones('krOkOdɪ:l', True))
        self.assertEqual(7, sk.count_phones('kUrI_^atkO', True))
        self.assertRaises(WordSegmentException, lambda word: sk.count_phones(word, True), 'kUrI^atkO')
        self.assertEqual(6, sk.count_phones('lavɪtsE', True))
        self.assertEqual(9, sk.count_phones('xɪll zEbra', True))

        self.assertListEqual(['k', 'U', 'r', 'I_^a', 't', 'k', 'O'], sk.get_phones_list('kUrI_^atkO', True))


class EN(TestCase):

    def test_letters(self):
        self.assertEqual(6, en.count_letters('dinner'))
        self.assertEqual(6, en.count_letters('devil\'s'))
        self.assertEqual(5, en.count_letters('dirty'))
        self.assertEqual(9, en.count_letters('non edible'))
        self.assertEqual(9, en.count_letters('Alice Rock'))
        self.assertEqual(11, en.count_letters('An Apple a Day'))

    def test_phones(self):
        self.assertEqual(9, en.count_phones('nɒnˈed.ə.bəl'))
        self.assertEqual(6, en.count_phones('mestˈʌp'))
        self.assertEqual(7, en.count_phones('ˈɑː.məd dʌk'))

