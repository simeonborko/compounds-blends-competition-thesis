from collections import OrderedDict

import pymysql
import csv
import configuration as c
from pymysql.constants import FIELD_TYPE


class Connection:

    def __enter__(self):

        conv = dict(pymysql.converters.conversions)
        conv[FIELD_TYPE.DECIMAL] = float
        conv[FIELD_TYPE.NEWDECIMAL] = float

        self.conn = pymysql.connect(
            host=c.HOST,
            port=c.PORT,
            user=c.USER,
            password=c.PASSWD,
            database=c.DB,
            conv=conv,
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class CorpConnection:

    def __enter__(self):

        conv = dict(pymysql.converters.conversions)
        conv[FIELD_TYPE.DECIMAL] = float
        conv[FIELD_TYPE.NEWDECIMAL] = float

        self.conn = pymysql.connect(
            host=c.CORP_HOST,
            port=c.CORP_PORT,
            user=c.CORP_USER,
            password=c.CORP_PASSWD,
            database=c.CORP_DB,
            conv=conv,
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def tsv_reader(fp):
    cr = csv.reader(fp, delimiter='\t')
    return map(lambda row: [c.strip() if len(c.strip()) > 0 else None for c in row], cr)


def get_res2lang(cursor) -> dict:
    """respondent_id => (first_language, survey_language)"""
    res2lang = {}
    cursor.execute('select respondent_id, first_language, survey_language from respondent')
    for r in cursor:
        res2lang[r[0]] = (r[1], r[2])
    return res2lang


def get_lang2code(cursor: iter) -> dict:
    """language name -> language code"""
    cursor.execute('Select name, code from language')
    return dict(cursor)


class Table:
    def __init__(self, key_fields: iter, other_fields: iter):
        self.key_fields = tuple(key_fields)
        self.other_fields = tuple(other_fields)
        self.field_set = set(list(self.key_fields) + list(self.other_fields))
        self.data = OrderedDict()

    def add(self, row: dict):

        # otestovat vstup
        if set(row.keys()) != self.field_set:
            raise Exception

        if len(row) != len(self.key_fields) + len(self.other_fields):
            raise Exception
        key = tuple([row[field] for field in self.key_fields])
        values = tuple([row[field] for field in self.other_fields])
        if key not in self.data:
            self.data[key] = tuple([set() for dummy in range(len(self.other_fields))])
        dtup = self.data[key]
        for i, val in enumerate(values):
            if val:
                dtup[i].add(val)

    def write(self, filename):
        with open('data/export/'+filename, 'w') as fp:
            wr = csv.writer(fp, delimiter='\t')
            wr.writerow([*self.key_fields, *self.other_fields])
            for k, v in self.data.items():
                if max([len(s) for s in v]) < 2:
                    continue
                wr.writerow([*k, *[' | '.join(s) if len(s) >= 2 else None for s in v]])


# table = Table(
#     ('k1', 'k2'),
#     ('v1', 'v2')
# )
#
# table.add({
#     'k1': '1',
#     'k2': '3',
#     'v1': '1',
#     'v2': '1'
# })
#
# table.add({
#     'k1': '1',
#     'k2': '3',
#     'v1': '1',
#     'v2': '2'
# })
#
# table.add({
#     'k1': '1',
#     'k2': '2',
#     'v1': '1',
#     'v2': '2'
# })
#
# table.write('demo.txt')




