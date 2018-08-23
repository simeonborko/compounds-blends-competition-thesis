from model import Overview
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

