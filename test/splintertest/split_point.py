from unittest import TestCase

from tools.splinter import SlovakGraphicSplinter, LexshType, SplitPointType, EnglishPhoneticSplinter


class SplitPointTest(TestCase):

    def __test_sk(self, nu_graphic, nu_syllabic, sw_graphic, ex_splinter, ex_lexsh, ex_split_point):
        s = SlovakGraphicSplinter(nu_graphic, sw_graphic, True)
        self.assertTrue(s.find_splinter())
        self.assertEqual(ex_splinter, s.splinter)
        self.assertEqual(ex_lexsh, s.lexical_shortening)
        self.assertEqual(
            ex_split_point,
            s.get_split_point(nu_syllabic)
        )

    # def test_sk_fsw_1a(self):
    #     self.__test_sk('Punkblko', 'Punk-bl-ko', 'punk', 'punk', LexshType.FSW, SplitPointType.SYLLABLE)

    def test_sk_fsw_1b(self):
        self.__test_sk('Punkblko', 'Punk-bl-ko', 'punk', 'punk', LexshType.FSW, None)

    # def test_sk_fsw_2a(self):
    #     self.__test_sk('punkblko', 'punk-bl-ko', 'punk', 'punk', LexshType.FSW, SplitPointType.SYLLABLE)

    def test_sk_fsw_2b(self):
        self.__test_sk('punkblko', 'punk-bl-ko', 'punk', 'punk', LexshType.FSW, None)

    def test_sk_krokacka(self):
        self.__test_sk('krokačka', 'kro-kač-ka', 'krokodíl', 'krok', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_rybociar(self):
        self.__test_sk('Rybočiar', 'Ry-bo-čiar', 'ryba', 'ryb', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('Rybočiar', 'Ry-bo-čiar', 'mravčiar', 'čiar', LexshType.LS, SplitPointType.SYLLABLE)

    def test_sk_punkblko(self):
        # self.__test_sk('Punkblko', 'Punk-bl-ko', 'punk', 'punk', LexshType.FSW, SplitPointType.SYLLABLE)
        self.__test_sk('Punkblko', 'Punk-bl-ko', 'jablko', 'blko', LexshType.LS, SplitPointType.SYLLABLE)

    def test_sk_zajomops(self):
        # self.__test_sk('Zajomops', 'Za-jo-mops', 'zajo', 'zajo', LexshType.FSW, SplitPointType.SYLLABLE)
        self.__test_sk('Zajomops', 'Za-jo-mops', 'zajac', 'zaj', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('Zajomops', 'Za-jo-mops', 'mopslík', 'mops', LexshType.RS, None)  # neviem, je to medzi "s" a "l"

    def test_sk_skalotav(self):
        self.__test_sk('skaloťav', 'ska-lo-ťav', 'skala', 'skal', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('skaloťav', 'ska-lo-ťav', 'ťava', 'ťav', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_mackoraf(self):
        self.__test_sk('Mačkoraf', 'Mač-ko-raf', 'mačka', 'mačk', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('Mačkoraf', 'Mač-ko-raf', 'žirafa', 'raf', LexshType.RSLS, None)

    def test_sk_blkostan(self):
        self.__test_sk('blkostan', 'bl-ko-stan', 'jablko', 'blko', LexshType.LS, SplitPointType.SYLLABLE)
        # self.__test_sk('blkostan', 'bl-ko-stan', 'stan', 'stan', LexshType.FSW, SplitPointType.SYLLABLE)  # alebo None?

    def test_sk_rolev(self):
        self.__test_sk('rolev', 'ro-lev', 'orol', 'rol', LexshType.LS, SplitPointType.NUCL_CODA)
        # self.__test_sk('rolev', 'ro-lev', 'lev', 'lev', LexshType.FSW, SplitPointType.SYLLABLE)

    def test_sk_vank(self):
        self.__test_sk('vank', 'vank', 'karavan', 'van', LexshType.LS, SplitPointType.SYLLABLE)
        self.__test_sk('vank', 'vank', 'tank', 'ank', LexshType.LS, SplitPointType.ONSET_NUCL)

    def test_sk_citrokocka(self):
        self.assertTrue(False)
        # self.__test_sk('citrokocka', 'ci-tro-koc-ka', 'citrón', 'citr', LexshType.RS, )

    def test_sk_chobozebra(self):
        self.__test_sk('chobozebra', 'cho-bo-zeb-ra', 'chobot', 'chobo', LexshType.RS, SplitPointType.NUCL_CODA)

    def test_sk_krokacica(self):
        self.__test_sk('krokačica', 'kro-ka-či-ca', 'krokodíl', 'krok', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_lastodelfin(self):
        self.__test_sk('lastodelfín', 'las-to-del-fín', 'lastovička', 'lasto', LexshType.RS, SplitPointType.SYLLABLE)

    def test_sk_koblak(self):
        # FIXME je Kôb-lak správne rozdelenie?
        self.__test_sk('Kôblak', 'Kôb-lak', 'kôň', 'kô', LexshType.RS, SplitPointType.NUCL_CODA)

    def test_sk_byvtank(self):
        self.__test_sk('Byvtank', 'Byv-tank', 'bývanie', 'býv', LexshType.RS, SplitPointType.ONSET_NUCL)

    def test_sk_kapanky(self):
        self.__test_sk('kapánky', 'ka-pán-ky', 'kaktus', 'ka', LexshType.RS, SplitPointType.NUCL_CODA)
        self.__test_sk('kapánky', 'ka-pán-ky', 'topánky', 'pánky', LexshType.LS, SplitPointType.SYLLABLE)

    def test_sk_kaktanky(self):
        self.__test_sk('kaktánky', 'kak-tán-ky', 'kaktus', 'kakt', LexshType.RS, SplitPointType.ONSET_NUCL)
        self.__test_sk('kaktánky', 'kak-tán-ky', 'topánky', 'ánky', LexshType.LS, SplitPointType.ONSET_NUCL)

    def test_sk_krokogaj(self):
        self.__test_sk('Krokogáj', 'Kro-ko-gáj', 'krokodíl', 'kroko', LexshType.RS, SplitPointType.SYLLABLE)
        self.__test_sk('Krokogáj', 'Kro-ko-gáj', 'papagáj', 'gáj', LexshType.RS, SplitPointType.SYLLABLE)

    def test_sk_kockoranc(self):
        self.assertTrue(False)
        # self.__test_sk('Kockoranč', 'Koc-ko-ranč', 'kocka', 'kock')

    def test_sk_kraes(self):
        self.assertTrue(False)
        # self.__test_sk('kraes', 'kra-es', 'králik')

    def __test_en(self, nu_phonetic, sw_phonetic, ex_splinter, ex_lexsh, ex_split_point):
        s = EnglishPhoneticSplinter(nu_phonetic, sw_phonetic, True)
        self.assertTrue(s.find_splinter())
        self.assertEqual(ex_splinter, s.splinter)
        self.assertEqual(ex_lexsh, s.lexical_shortening)
        self.assertEqual(
            ex_split_point,
            s.get_split_point(nu_phonetic)
        )

    def test_en_1(self):
        self.__test_en('ˈæl.ɪ.ɡwɪn', 'ˈæl.ɪ.ɡeɪ.tər', 'æ l ɪ ɡ', LexshType.RS, SplitPointType.ONSET_NUCL)
    'dʒɪˈruːs'
