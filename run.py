from collections import OrderedDict
from tkinter import messagebox
from tkinter import *

from openpyxl import Workbook, load_workbook
from os.path import isfile

from model import ImageTable, LanguageTable, NamingUnitTable, RespondentTable, ResponseTable, SourceWordTable, SplinterTable
from tools import Connection, ListSaver
import configuration


TABLES = (ImageTable, LanguageTable, NamingUnitTable, RespondentTable, ResponseTable, SourceWordTable, SplinterTable)


def export():

    if isfile(configuration.XLSX_FILE):
        messagebox.showerror('Chyba', 'Súbor {} už existuje'.format(configuration.XLSX_FILE))
        return

    wb = Workbook()
    with Connection() as conn:
        for table in TABLES:
            table(wb, conn).create_sheet()

    wb.remove(wb['Sheet'])
    wb.save(configuration.XLSX_FILE)

    messagebox.showinfo(
        'Vytvorenie dokumentu',
        'Dokument vytvorený:\n\n' + configuration.XLSX_FILE
    )


def sync():

    if not isfile(configuration.XLSX_FILE):
        messagebox.showerror('Chyba', 'Súbor {} neexistuje'.format(configuration.XLSX_FILE))
        return

    tables = selected_tables()
    if len(tables) == 0:
        messagebox.showwarning(
            'Synchronizácia',
            'Neboli vybrané žiadne tabuľky'
        )
        return

    wb = load_workbook(configuration.XLSX_FILE)
    with Connection() as conn:
        for table in tables:
            table(wb, conn).sync()
        conn.commit()

    wb.save(configuration.XLSX_FILE)

    messagebox.showinfo(
        'Synchronizácia',
        'Synchronizované:\n\n' + '\n'.join('- ' + table.name() for table in tables)
    )


def generate():
    if not isfile(configuration.XLSX_FILE):
        messagebox.showerror('Chyba', 'Súbor {} neexistuje'.format(configuration.XLSX_FILE))
        return

    generable = (NamingUnitTable, SourceWordTable)

    tables = set(selected_tables()) & set(generable)
    if len(tables) == 0:
        messagebox.showwarning(
            'Automatizované vyplnenie',
            'Automatizovane vyplniť sa dajú iba tieto tabuľky:\n\n' + '\n'.join('- ' + table.name() for table in generable)
        )
        return

    force = bool(force_var.get())
    corpus = bool(corpus_var.get())

    affected = OrderedDict()

    wb = load_workbook(configuration.XLSX_FILE)
    with Connection() as conn:
        for table in tables:
            t = table(wb, conn)
            t.sync()
            affected[table.name()] = t.generate(force=force, corpus=corpus)
            t.sync()
        conn.commit()
    wb.save(configuration.XLSX_FILE)

    messagebox.showinfo(
        'Automatizované vyplnenie',
        'Automatizovane vyplnené a synchronizované:\n\n{}\n\nAj už vyplnené: {}\nKorpus: {}'.format(
            '\n'.join('- {} ({})'.format(tablename, aff) for tablename, aff in affected.items()),
            'Áno' if force else 'Nie',
            'Áno' if corpus else 'Nie'
        )
    )


def integrity():
    if not isfile(configuration.XLSX_FILE):
        messagebox.showerror('Chyba', 'Súbor {} neexistuje'.format(configuration.XLSX_FILE))
        return

    integritable = (NamingUnitTable, SourceWordTable)

    tables = set(selected_tables()) & set(integritable)
    if len(tables) == 0:
        messagebox.showwarning(
            'Kontrola súdržnosti',
            'Kontrolovať sa dajú iba tieto tabuľky:\n\n' + '\n'.join('- ' + table.name() for table in integritable)
        )
        return

    affected = OrderedDict()

    wb = load_workbook(configuration.XLSX_FILE)
    with Connection() as conn:
        for table in tables:
            t = table(wb, conn)
            t.sync()
            added = t.integrity_add()
            removed = t.integrity_junk()
            affected[table.name()] = (added, removed)
            t.sync()
        conn.commit()
    wb.save(configuration.XLSX_FILE)

    messagebox.showinfo(
        'Kontrola súdržnosti',
        'Skontrolované a synchronizované:\n\n{}\n\nOdobrané riadky sú v tabuľke `junk [názov tabuľky]`'.format(
            '\n'.join('- {} (pridané: {}, odobrané: {})'.format(tablename, *a) for tablename, a in affected.items()),
        )
    )


checkvars = []


def selected_tables():
    return [TABLES[i] for i, var in enumerate(checkvars) if var.get() == 1]


if not configuration.TKINTER_TRACEBACK:
    Tk.report_callback_exception = lambda obj, exc, val, tb: print(val, file=sys.stderr)

with ListSaver(configuration.CHECKBOX_FILE, [1] * len(TABLES)) as saver:
    mw = Tk()
    mw.wm_title("Workbook Tlačítka")
    force_var = IntVar(value=1)
    corpus_var = IntVar(value=0)

    for i, value in enumerate(saver):
        var = IntVar(value=value)
        checkvars.append(var)
        Checkbutton(mw, text=TABLES[i].name(), variable=var).grid(row=i, column=0, sticky=W, padx=(0, 30), pady=2)

    Button(
        mw,
        text='Vytvoriť dokument',
        command=export,
    ).grid(row=0, column=1, padx=5, pady=5, rowspan=2, sticky=E+W)

    Button(
        mw,
        text='Synchronizovať',
        command=sync,
    ).grid(row=2, column=1, padx=5, pady=5, rowspan=2, sticky=E+W)

    Button(
        mw,
        text='Vyplniť automatizovane',
        command=generate
    ).grid(row=4, column=1, padx=5, pady=5, rowspan=2, sticky=E+W)
    Checkbutton(mw, text='Aj už vyplnené', variable=force_var).grid(row=4, column=2)
    Checkbutton(mw, text='Korpus', variable=corpus_var).grid(row=5, column=2)

    Button(
        mw,
        text='Kontrola súdržnosti',
        command=integrity
    ).grid(row=6, column=1, padx=5, pady=5, rowspan=2, sticky=E+W)

    mw.mainloop()

    for i, var in enumerate(checkvars):
        saver[i] = var.get()
