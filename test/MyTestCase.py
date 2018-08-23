from unittest import TestCase

from openpyxl import Workbook

import configuration as c

import pymysql


class MyTestCase(TestCase):

    conn = None
    wb = Workbook()

    @classmethod
    def setUpClass(cls):
        cls.conn = pymysql.connect(
            host=c.HOST,
            port=c.PORT,
            user='blanksimeon',
            password=c.PASSWD,
            database='blanksimeon'
        )

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
