from model import Overview, SourceWordTable, SplinterView
from test import MyTestCase


class SyncTestCase(MyTestCase):

    def test_overview_change_primary(self):

        overview = Overview(self.wb, self.conn)
        self.assertTrue(overview.create_sheet())

        sheet = self.wb[overview.name()]

        idx = {f: overview.fields.index(f) for f in ('respondent_id', 'nu_graphic', 'image_id', 'sw1_graphic')}

        # zmenim respondent_id na neexistujuce, mal by sa pridat novy riadok
        self.assertEqual(5, sheet.max_row)
        self.assertFalse(overview.sync())
        self.assertEqual(5, sheet.max_row)
        next(sheet.iter_rows(min_row=2))[idx['respondent_id']].value = 3000
        self.assertTrue(overview.sync())
        self.assertEqual(6, sheet.max_row)

    def test_overview_change_normal(self):

        overview = Overview(self.wb, self.conn)
        self.assertTrue(overview.create_sheet())
        self.assertFalse(overview.create_sheet())

        idx = {f: overview.fields.index(f) for f in ('respondent_id', 'nu_graphic', 'image_id', 'sw1_graphic')}

        sheet = self.wb[overview.name()]

        # zmenim sw1_graphic v SHEETE, mala by sa zrusit tato zmena
        cell = next(sheet.iter_rows(min_row=3))[idx['sw1_graphic']]
        origval = cell.value
        self.assertNotEqual(origval, 'slon')
        cell.value = 'slon'
        self.assertTrue(overview.sync())
        self.assertEqual(origval, cell.value)
        self.assertFalse(overview.sync())

    def test_table_change_primary(self):

        tbl = SourceWordTable(self.wb, self.conn)
        self.assertTrue(tbl.create_sheet())
        self.assertFalse(tbl.create_sheet())
        sheet = self.wb[tbl.name()]
        cell = next(sheet.iter_rows(min_row=2))[0]
        newval = 'PRIMARY CHANGED'
        self.assertNotEqual(newval, cell.value)
        cell.value = newval
        numb_of_rows = sheet.max_row
        self.assertTrue(tbl.sync())
        self.assertEqual(numb_of_rows + 1, sheet.max_row)
        self.assertFalse(tbl.sync())

    def test_table_change_editable(self):
        tbl = SourceWordTable(self.wb, self.conn)
        self.assertTrue(tbl.create_sheet())
        sheet = self.wb[tbl.name()]
        row = None
        for prow in sheet.iter_rows(min_row=2):
            if prow[0].value == 'motyl':
                row = prow
        self.assertIsNotNone(row)

        cell = row[tbl.fields.index('sw_phonetic')]
        self.assertEqual('motil', cell.value)
        cell.value = 'motilik'
        self.assertTrue(tbl.sync())
        self.assertEqual('motilik', cell.value)

        c = self.conn.cursor()
        query = "SELECT COUNT(*) FROM source_word WHERE sw_graphic=%s AND sw_phonetic=%s"
        c.execute(query, ('motyl', 'motil'))
        self.assertEqual(0, c.fetchone()[0])
        c.execute(query, ('motyl', 'motilik'))
        self.assertEqual(1, c.fetchone()[0])

        self.assertFalse(tbl.sync())

    def test_table_change_generated(self):
        tbl = SourceWordTable(self.wb, self.conn)
        self.assertTrue(tbl.create_sheet())
        sheet = self.wb[tbl.name()]
        row = None
        for prow in sheet.iter_rows(min_row=2):
            if prow[0].value == 'motyl':
                row = prow
        self.assertIsNotNone(row)

        cell = row[tbl.fields.index('G_sw_syllabic')]
        self.assertEqual('mo-tyl', cell.value)
        cell.value = 'CHYBA'
        self.assertTrue(tbl.sync())
        self.assertEqual('mo-tyl', cell.value)

        c = self.conn.cursor()
        query = "SELECT COUNT(*) FROM source_word WHERE sw_graphic=%s AND G_sw_syllabic=%s"
        c.execute(query, ('motyl', 'CHYBA'))
        self.assertEqual(0, c.fetchone()[0])
        c.execute(query, ('motyl', 'mo-tyl'))
        self.assertEqual(1, c.fetchone()[0])

        self.assertFalse(tbl.sync())

    def test_table_change_both(self):
        tbl = SourceWordTable(self.wb, self.conn)
        self.assertTrue(tbl.create_sheet())
        sheet = self.wb[tbl.name()]
        row = None
        for prow in sheet.iter_rows(min_row=2):
            if prow[0].value == 'motyl':
                row = prow
        self.assertIsNotNone(row)

        cells = (
            row[tbl.fields.index('sw_syllabic')],
            row[tbl.fields.index('G_sw_syllabic')],
        )

        cells[0].value = 'CHYBA'
        cells[1].value = 'CHYBA'

        self.assertTrue(tbl.sync())

        c = self.conn.cursor()
        c.execute("SELECT sw_syllabic, G_sw_syllabic FROM source_word WHERE sw_graphic=%s", ('motyl',))
        self.assertEqual(1, c.rowcount)
        self.assertTupleEqual(('CHYBA', 'mo-tyl'), c.fetchone())

        self.assertTupleEqual(('CHYBA', 'mo-tyl'), tuple(c.value for c in cells))

        self.assertFalse(tbl.sync())


class SplinterViewSyncTestCase(MyTestCase):

    def setUp(self):
        super().setUp()
        self.view = SplinterView(self.wb, self.conn)
        self.assertTrue(self.view.create_sheet())
        self.assertFalse(self.view.create_sheet())
        self.sheet = self.wb[self.view.name()]
        self.row = next(self.sheet.iter_rows(min_row=2))

    def tearDown(self):
        super().tearDown()
        self.assertFalse(self.view.sync())

    def __change_row_vals(self, vals: dict):
        orig = {}
        for name, val in vals.items():
            cell = self.row[self.view.fields.index(name)]
            orig[name] = cell.value
            self.assertNotEqual(val, cell.value)
            cell.value = val
        return orig

    def __get_row_vals(self, keys):
        return {k: self.row[self.view.fields.index(k)].value for k in keys}

    def __testvals(self, newvals, shouldrevert):
        origvals = self.__change_row_vals(newvals)
        self.assertNotEqual(newvals, origvals)
        self.assertTrue(self.view.sync())
        if shouldrevert:
            self.assertEqual(origvals, self.__get_row_vals(newvals.keys()))
        else:
            self.assertEqual(newvals, self.__get_row_vals(newvals.keys()))

    def test_primary(self):
        numb_of_rows = self.sheet.max_row
        self.__testvals({'nu_graphic': 'PRIMARY CHANGED'}, False)
        self.assertEqual(numb_of_rows + 1, self.sheet.max_row)

    def test_nu_editable(self):
        self.__testvals({
            'nu_phonetic': 'CHYBA',
            'nu_word_class': 'CH'
        }, False)

    def test_nu_static(self):
        self.__testvals({'G_nu_syllabic': 10}, True)

    def test_img(self):
        self.__testvals({'sub_sem_cat': 'CHYBA0'}, True)

    def test_sw(self):
        self.__testvals({
            'sw1_graphic': 'CHYBA',
            'sw1_source_language': 'CH'
        }, True)

    def test_spl_editable(self):
        self.__testvals({'gs_sw1_splinter': 'FILLED'}, False)

    def test_spl_static(self):
        self.__testvals({'gs_name': 'CHYBA'}, True)


