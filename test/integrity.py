from model import LanguageTable, NamingUnitTable, SourceWordTable, SplinterTable
from test import MyTestCase


class Language(MyTestCase):

    def test(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM language WHERE code=%s', ('SK',))
        c.execute('INSERT INTO language VALUES (%s, %s)', ('RU', 'Russian'))

        tbl = LanguageTable(self.wb, self.conn)
        self.assertEqual(1, tbl.integrity_add())
        self.assertEqual(1, tbl.integrity_junk())

        c.execute('SELECT code, name FROM language')
        self.assertEqual(1, c.rowcount)
        self.assertTupleEqual(('SK', None), c.fetchone())


class NamingUnit(MyTestCase):

    def test(self):

        tbl = NamingUnitTable(self.wb, self.conn)
        self.assertEqual(0, tbl.integrity_add())
        self.assertEqual(1, tbl.integrity_junk())

        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM naming_unit')
        self.assertEqual(3, c.fetchone()[0])

        sheet = self.wb['junk naming_unit']
        self.assertEqual(2, sheet.max_row)
        self.assertEqual('Aragátor', next(sheet.iter_rows(min_row=2))[0].value)


class SourceWord(MyTestCase):

    def test(self):

        c = self.conn.cursor()
        c.execute('UPDATE source_word SET first_language=%s WHERE sw_graphic = %s', ('ne', 'kacka'))

        tbl = SourceWordTable(self.wb, self.conn)
        self.assertEqual(1, tbl.integrity_add())
        self.assertEqual(1, tbl.integrity_junk())

        c.execute('SELECT first_language FROM source_word WHERE sw_graphic=%s', ('kacka',))
        self.assertEqual(1, c.rowcount)
        self.assertEqual('SK', c.fetchone()[0])

        sheet = self.wb['junk source_word']
        self.assertEqual(2, sheet.max_row)
        row = next(sheet.iter_rows(min_row=2))
        self.assertEqual('kacka', row[0].value)
        self.assertEqual('ne', row[tbl.fields.index('first_language')].value)


class Splinter(MyTestCase):

    def test(self):

        tbl = SplinterTable(self.wb, self.conn)
        self.assertEqual(4, tbl.integrity_add())
        self.assertEqual(0, tbl.integrity_junk())
