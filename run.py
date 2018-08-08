from openpyxl import Workbook, load_workbook
from os.path import isfile

from table import ImageTable, LanguageTable, NamingUnitTable, RespondentTable, ResponseTable, SourceWordTable, SplinterTable
from tools.tools import Connection
import configuration

from tkinter import *

TABLES = (ImageTable, LanguageTable, NamingUnitTable, RespondentTable, ResponseTable, SourceWordTable, SplinterTable)


def export():

    if isfile(configuration.XLSX_FILE):
        raise Exception('Subor {} uz existuje'.format(configuration.XLSX_FILE))

    wb = Workbook()
    with Connection() as conn:
        for table in TABLES:
            table(wb, conn).create_sheet()

    wb.remove(wb['Sheet'])
    wb.save(configuration.XLSX_FILE)


def sync():

    if not isfile(configuration.XLSX_FILE):
        raise Exception('Subor {} neexistuje'.format(configuration.XLSX_FILE))

    wb = load_workbook(configuration.XLSX_FILE)
    with Connection() as conn:
        for table in TABLES:
            table(wb, conn).sync()
        conn.commit()

    wb.save(configuration.XLSX_FILE)


mw = Tk()
mw.geometry("300x100")
Button(mw, text='Vytvoriť dokument', command=export).pack()
Button(mw, text='Synchronizovať', command=sync).pack()
mw.mainloop()

