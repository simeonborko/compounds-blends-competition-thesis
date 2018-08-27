from model import NamingUnitTable, SourceWordTable, SplinterTable
from test import MyTestCase


class GenerateTestCase(MyTestCase):

    def test_namingunit(self):
        tbl = NamingUnitTable(self.wb, self.conn)
        self.assertEqual(4, tbl.generate(False))
        self.assertEqual(0, tbl.generate(False))
        self.assertEqual(0, tbl.generate(True))

        cursor = self.conn.cursor()
        cursor.execute("SELECT G_nu_syllabic, G_nu_graphic_len, G_nu_phonetic_len, G_nu_syllabic_len FROM naming_unit WHERE nu_graphic = %s", ('Aragátor',))
        self.assertEqual(1, cursor.rowcount)
        row = cursor.fetchone()
        self.assertTupleEqual(('A-ra-gá-tor', 8, 8, 4), row)

        self.assertTrue(tbl.create_sheet())

        row = next(filter(lambda row: row[0].value == 'krokacka', self.wb[tbl.name()].iter_rows(min_row=2)))
        self.assertEqual('kro-kac-ka', row[tbl.fields.index('G_nu_syllabic')].value)
        self.assertEqual(8, row[tbl.fields.index('G_nu_graphic_len')].value)
        self.assertEqual(None, row[tbl.fields.index('G_nu_phonetic_len')].value)
        self.assertEqual(3, row[tbl.fields.index('G_nu_syllabic_len')].value)

    def test_sourceword(self):
        tbl = SourceWordTable(self.wb, self.conn)
        self.assertEqual(4, tbl.generate(False, corpus=False))

        cursor = self.conn.cursor()
        cursor.execute("SELECT G_sw_syllabic, G_sw_graphic_len, G_sw_phonetic_len, G_sw_syllabic_len, frequency_in_snc FROM source_word WHERE sw_graphic=%s", ('kacka',))
        self.assertEqual(1, cursor.rowcount)
        row = cursor.fetchone()
        self.assertTupleEqual(('kac-ka', 5, 5, 2, None), row)

        self.assertEqual(4, tbl.generate(False, corpus=True))

        cursor.execute("SELECT frequency_in_snc FROM source_word WHERE sw_graphic = %s", ('kacka',))
        self.assertEqual(4, cursor.fetchone()[0])

    def test_splinter(self):
        tbl = SplinterTable(self.wb, self.conn)
        self.assertTrue(tbl.generate(False) > 0)
        cursor = self.conn.cursor()
        cursor.execute("SELECT G_sw1_splinter, G_sw1_splinter_len FROM splinter WHERE nu_graphic=%s AND type_of_splinter=%s",
                       ('krokacka', 'graphic strict'))
        self.assertTupleEqual(('krok', 4), cursor.fetchone())
