from model import Overview, ImageTable, SplinterView
from test import MyTestCase


class ExportTestCase(MyTestCase):

    def test_overview(self):
        overview = Overview(self.wb, self.conn)
        self.assertTrue(overview.create_sheet())
        sheet = self.wb[overview.name()]
        self.assertEqual(5, sheet.max_row)
        idx = overview.fields.index('nu_graphic')
        self.assertEqual(
            sorted(['krokacka', 'zirafomotyl', 'krokacka', 'motylozirafa']),
            sorted([row[idx].value for row in sheet.iter_rows(min_row=2)])
        )
        self.assertFalse(overview.create_sheet())

    def test_table(self):
        img = ImageTable(self.wb, self.conn)
        self.assertTrue(img.create_sheet())
        sheet = self.wb[img.name()]
        self.assertEqual(3, sheet.max_row)

        img_id = img.fields.index('image_id')
        sub_sem = img.fields.index('sub_sem_cat')
        dom_sem = img.fields.index('dom_sem_cat')

        self.assertEqual(
            {
                1: ('animal', 'thing'),
                2: ('thing', 'animal')
            },
            {
                int(row[img_id].value): (row[sub_sem].value, row[dom_sem].value)
                for row in sheet.iter_rows(min_row=2)
            }
        )

        self.assertFalse(img.create_sheet())

    def test_splinterview(self):
        view = SplinterView(self.wb, self.conn)
        self.assertTrue(view.create_sheet())
        self.assertFalse(view.create_sheet())
        sheet = self.wb[view.name()]
        self.assertEqual(5, sheet.max_row)

        nu_idx = view.fields.index('nu_graphic')
        img_idx = view.fields.index('image_id')

        self.assertEqual(
            sorted([
                ('Aragátor', 7),
                ('krokacka', 1),
                ('motylozirafa', 2),
                ('zirafomotyl', 2)
            ]),
            sorted([(row[nu_idx].value, int(row[img_idx].value)) for row in sheet.iter_rows(min_row=2)])
        )

