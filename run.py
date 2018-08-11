from openpyxl import Workbook, load_workbook
from os.path import isfile

from table import ImageTable, LanguageTable, NamingUnitTable, RespondentTable, ResponseTable, SourceWordTable, SplinterTable
from tools import Connection, ListSaver
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

    tables = selected_tables()
    if len(tables) == 0:
        return

    wb = load_workbook(configuration.XLSX_FILE)
    with Connection() as conn:
        for table in tables:
            table(wb, conn).sync()
        conn.commit()

    wb.save(configuration.XLSX_FILE)


checkvars = []


def selected_tables():
    return [TABLES[i] for i, var in enumerate(checkvars) if var.get() == 1]


if not configuration.TKINTER_TRACEBACK:
    Tk.report_callback_exception = lambda obj, exc, val, tb: print(val, file=sys.stderr)

with ListSaver(configuration.JSON_FILE, [1] * len(TABLES)) as saver:
    mw = Tk()
    mw.wm_title("Workbook Tlačítka")

    Button(
        mw,
        text='Vytvoriť dokument',
        command=export,
    ).grid(row=0, column=0, padx=5, pady=(5, 10), columnspan=2)

    for i, value in enumerate(saver):
        var = IntVar(value=value)
        checkvars.append(var)
        Checkbutton(mw, text=TABLES[i].name(), variable=var).grid(row=i+1, column=0, sticky=W, padx=(0, 30), pady=2)

    Button(
        mw,
        text='Synchronizovať',
        command=sync,
    ).grid(row=1, column=1, padx=5, pady=5, rowspan=2, sticky=E+W)
    Button(
        mw,
        text='Vyplniť automatizovane',
        command=lambda: print(selected_tables())
    ).grid(row=3, column=1, padx=5, pady=5, rowspan=2, sticky=E+W)
    Button(
        mw,
        text='Kontrola súdržnosti',
    ).grid(row=5, column=1, padx=5, pady=5, rowspan=2, sticky=E+W)

    mw.mainloop()

    for i, var in enumerate(checkvars):
        saver[i] = var.get()
