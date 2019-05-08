from unittest import TestCase

from tools.splinter import SlovakGraphicSplinter, LexshType, SplitPointType, EnglishPhoneticSplinter


class SplitPointTest(TestCase):

    def __test_sk(self, nu_graphic, sw_graphic, sw_phonetic, ex_splinter, ex_lexsh, ex_split_point):
        s = SlovakGraphicSplinter(nu_graphic, sw_graphic, True)
        self.assertTrue(s.find_splinter())
        self.assertEqual(ex_splinter, s.splinter)
        self.assertEqual(ex_lexsh, s.lexical_shortening)
        self.assertEqual(
            ex_split_point,
            s.get_split_point(sw_phonetic)
        )

    def test_sk_fsw_1(self):
        self.__test_sk('Punkblko', 'punk', 'punk', 'punk', LexshType.FSW, None)

    def test_sk_fsw_2(self):
        self.__test_sk('punkblko', 'punk', 'punk', 'punk', LexshType.FSW, None)

    def test_sk_krokacka(self):
        self.__test_sk('krokačka', 'krokodíl',  'kro-ko-díl', 'krok', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_rybociar(self):
        self.__test_sk('Rybočiar', 'ryba', 'ry-ba', 'ryb', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('Rybočiar', 'mravčiar', 'mrav-čiar', 'čiar', LexshType.LS, SplitPointType.SYLLABLE)

    def test_sk_punkblko(self):
        # self.__test_sk('Punkblko', 'punk', 'punk', 'punk', LexshType.FSW, SplitPointType.SYLLABLE)
        self.__test_sk('Punkblko', 'jablko', 'ja-bl-ko', 'blko', LexshType.LS, SplitPointType.SYLLABLE)

    def test_sk_zajomops(self):
        # self.__test_sk('Zajomops', 'zajo', 'Za-jo-mops', 'zajo', LexshType.FSW, SplitPointType.SYLLABLE)
        self.__test_sk('Zajomops', 'zajac', 'za-jac', 'zaj', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('Zajomops', 'mopslík', 'mop-slík', 'mops', LexshType.RS, None)  # neviem, je to medzi "s" a "l"

    def test_sk_skalotav(self):
        self.__test_sk('skaloťav', 'skala', 'ska-la', 'skal', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('skaloťav', 'ťava', 'ťa-va', 'ťav', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_mackoraf(self):
        self.__test_sk('Mačkoraf', 'mačka', 'mač-ka', 'mačk', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('Mačkoraf', 'žirafa', 'ži-ra-fa', 'raf', LexshType.RSLS, None)

    def test_sk_blkostan(self):
        self.__test_sk('blkostan', 'jablko', 'ja-bl-ko', 'blko', LexshType.LS, SplitPointType.SYLLABLE)
        # self.__test_sk('blkostan', 'stan', 'bl-ko-stan', 'stan', LexshType.FSW, SplitPointType.SYLLABLE)  # alebo None?

    def test_sk_rolev(self):
        self.__test_sk('rolev', 'orol', 'o-rol', 'rol', LexshType.LS, SplitPointType.NUCL_CODA)
        # self.__test_sk('rolev', 'lev', 'ro-lev', 'lev', LexshType.FSW, SplitPointType.SYLLABLE)

    def test_sk_vank(self):
        self.__test_sk('vank', 'karavan', 'ka-ra-van', 'van', LexshType.LS, SplitPointType.SYLLABLE)
        self.__test_sk('vank', 'tank', 'tank', 'ank', LexshType.LS, SplitPointType.ONSET_NUCL)

    def test_sk_citrokocka(self):
        self.assertTrue(False)
        # self.__test_sk('citrokocka', 'citrón', 'cit-rón', 'citr', LexshType.RS, )

    def test_sk_chobozebra(self):
        self.__test_sk('chobozebra', 'chobot', 'cho-bot', 'chobo', LexshType.RS, SplitPointType.NUCL_CODA)

    def test_sk_krokacica(self):
        self.__test_sk('krokačica', 'krokodíl', 'kro-ko-díl', 'krok', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_lastodelfin(self):
        self.__test_sk('lastodelfín', 'lastovička', 'las-to-vič-ka', 'lasto', LexshType.RS, SplitPointType.SYLLABLE)

    def test_sk_koblak(self):
        self.__test_sk('Kôblak', 'kôň', 'kôn', 'kô', LexshType.RS, SplitPointType.NUCL_CODA)

    def test_sk_byvtank(self):
        self.__test_sk('Byvtank', 'bývanie', 'bý-va-nie', 'býv', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_kapanky(self):
        self.__test_sk('kapánky', 'kaktus', 'kak-tus', 'ka', LexshType.RS, SplitPointType.NUCL_CODA)
        self.__test_sk('kapánky', 'topánky', 'to-pán-ky', 'pánky', LexshType.LS, SplitPointType.SYLLABLE)

    def test_sk_kaktanky(self):
        self.__test_sk('kaktánky', 'kaktus', 'kak-tus', 'kakt', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('kaktánky', 'topánky', 'to-pán-ky', 'ánky', LexshType.LS, SplitPointType.ONSET_NUCL)

    def test_sk_krokogaj(self):
        self.__test_sk('Krokogáj', 'krokodíl', 'kro-ko-díl', 'kroko', LexshType.RS, SplitPointType.SYLLABLE)
        self.__test_sk('Krokogáj', 'papagáj', 'pa-pa-gáj', 'gáj', LexshType.RS, SplitPointType.SYLLABLE)

    def test_sk_kockoranc(self):
        self.assertTrue(False)
        # self.__test_sk('Kockoranč', 'kocka', 'Koc-ko-ranč', 'kock')

    def test_sk_kraes(self):
        self.assertTrue(False)
        # self.__test_sk('kraes', 'králik', 'kra-es')

    def __test_en(self, nu_phonetic, sw_phonetic, ex_splinter, ex_lexsh, ex_split_point):
        s = EnglishPhoneticSplinter(nu_phonetic, sw_phonetic, True)
        self.assertTrue(s.find_splinter())
        self.assertEqual(ex_splinter, s.splinter)
        self.assertEqual(ex_lexsh, s.lexical_shortening)
        self.assertEqual(
            ex_split_point,
            s.get_split_point(sw_phonetic)
        )

    def test_en_1(self):
        self.__test_en('ˈæl.ɪ.ɡwɪn', 'ˈæl.ɪ.ɡeɪ.tər', 'æ l ɪ ɡ', LexshType.RS, SplitPointType.ONSET_NUCL)
    'dʒɪˈruːs'
