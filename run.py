import threading
from enum import Enum
from tkinter import *

from varmanager import VarManager
from widgetmanager import WidgetManager
from model import ImageTable, LanguageTable, NamingUnitTable, RespondentTable, SourceWordTable, \
    SplinterTable, SplinterView, Overview, ResponseView
import configuration
import worker


SYNC_CLSS = (ImageTable, LanguageTable, NamingUnitTable, RespondentTable, SourceWordTable, SplinterTable)
GEN_CLSS = (
    NamingUnitTable,
    SourceWordTable,
    SplinterTable
)
INTEG_CLSS = (LanguageTable, NamingUnitTable, SourceWordTable, SplinterTable)

widgetmanager = WidgetManager()


class Group(Enum):
    UNHIGHLIGHT = 0
    SYNC = 1
    GEN = 2
    OPTIONS = 3
    INTEG = 4


def unhighlight() -> bool:
    return varmanager[Group.UNHIGHLIGHT][0]


def export():
    threading.Thread(target=worker.export, args=(SYNC_CLSS, widgetmanager.widgets)).start()


def sync():
    clss = [SYNC_CLSS[i] for i in varmanager[Group.SYNC]]
    threading.Thread(target=worker.sync, args=(clss, unhighlight(), widgetmanager.widgets)).start()


def generate():
    clss = [GEN_CLSS[i] for i in varmanager[Group.GEN]]
    vargroup = varmanager[Group.OPTIONS]
    threading.Thread(target=worker.generate, args=(clss, unhighlight(), vargroup[0], vargroup[1], widgetmanager.widgets)).start()


def integrity():
    clss = [INTEG_CLSS[i] for i in varmanager[Group.INTEG]]
    threading.Thread(target=worker.integrity, args=(clss, unhighlight(), widgetmanager.widgets)).start()


def splinterview():
    threading.Thread(target=worker.splinterview, args=(SplinterView, unhighlight(), widgetmanager.widgets)).start()


def overview():
    threading.Thread(target=worker.overview, args=(Overview, unhighlight(), widgetmanager.widgets)).start()


def responseview():
    threading.Thread(target=worker.responseview, args=(ResponseView, unhighlight(), widgetmanager.widgets)).start()


if not configuration.TKINTER_TRACEBACK:
    Tk.report_callback_exception = lambda obj, exc, val, tb: print(val, file=sys.stderr)


def make_line(parent, row):
    Frame(parent, highlightbackground="#aaaaaa", highlightcolor="#aaaaaa", highlightthickness=1, height=1.5).grid(
        row=row, column=0, sticky=W + E, columnspan=2, padx=5
    )

# framecls = Frame
# Frame = lambda mw: framecls(mw, highlightbackground="gray", highlightcolor="gray", highlightthickness=1, bd=0)


buttoncls = Button
checkercls = Checkbutton


def Button(*args, **kwargs): return widgetmanager.button(buttoncls, args, kwargs)


def Checkbutton(*args, **kwargs): return widgetmanager.checker(checkercls, args, kwargs)


with VarManager(configuration.CHECKBOX_FILE) as varmanager:
    mw = Tk()
    mw.wm_title("Workbook Tlačítka")

    row = 0

    exportFrame = Frame(mw)
    exportFrame.grid(row=row, column=0, columnspan=2, sticky=W+E, pady=10, padx=10)

    row += 1
    make_line(mw, row)
    row += 1

    highlightFrame = Frame(mw)
    highlightFrame.grid(row=row, column=0, columnspan=2, sticky=W+E, pady=10, padx=10)

    row += 1
    make_line(mw, row)
    row += 1

    syncLeftFrame = Frame(mw)
    syncLeftFrame.grid(row=row, column=0, pady=10, padx=10)
    syncRightFrame = Frame(mw)
    syncRightFrame.grid(row=row, column=1, pady=10, padx=10, sticky=W)

    row += 1
    make_line(mw, row)
    row += 1

    generateLeftFrame = Frame(mw)
    generateLeftFrame.grid(row=row, column=0, pady=10, padx=10)
    generateRightFrame = Frame(mw)
    generateRightFrame.grid(row=row, column=1, pady=10, padx=10, sticky=W)

    row += 1
    make_line(mw, row)
    row += 1

    integrityLeftFrame = Frame(mw)
    integrityLeftFrame.grid(row=row, column=0, pady=10, padx=10)
    integrityRightFrame = Frame(mw)
    integrityRightFrame.grid(row=row, column=1, pady=10, padx=10, sticky=W)

    row += 1
    make_line(mw, row)
    row += 1

    viewFrame = Frame(mw)
    viewFrame.grid(row=row, column=0, columnspan=2, sticky=W+E, pady=10, padx=10)

    # export
    testbutton = Button(exportFrame, text='Exportovať', command=export)
    testbutton.pack(padx=10, pady=10)

    # highlight
    Checkbutton(
        highlightFrame, text='Zrušiť zvýraznenie minulých zmien', variable=varmanager.group(Group.UNHIGHLIGHT).var()
    ).pack()

    # sync
    vg = varmanager.group(Group.SYNC)
    for i, cls in enumerate(SYNC_CLSS):
        Checkbutton(syncLeftFrame, text=cls.name(), variable=vg.var()).grid(row=i, sticky=W, padx=(0, 30), pady=2)
    Button(syncRightFrame, text='Synchronizovať', command=sync).pack(padx=10, pady=10)

    # generate
    vg = varmanager.group(Group.GEN)
    for i, cls in enumerate(GEN_CLSS):
        Checkbutton(generateLeftFrame, text=cls.name(), variable=vg.var()).grid(row=i, sticky=W, padx=(0, 30), pady=2)
    Button(generateRightFrame, text='Vyplniť automatizovane', command=generate).grid(padx=10, pady=10, row=0, column=0, rowspan=2)
    vg = varmanager.group(Group.OPTIONS)
    Checkbutton(generateRightFrame, text='Aj už vyplnené', variable=vg.var()).grid(row=0, column=1, sticky=W)
    Checkbutton(generateRightFrame, text='Korpus', variable=vg.var()).grid(row=1, column=1, sticky=W)

    # integrity
    vg = varmanager.group(Group.INTEG)
    for i, cls in enumerate(INTEG_CLSS):
        Checkbutton(integrityLeftFrame, text=cls.name(), variable=vg.var()).grid(row=i, sticky=W, padx=(0, 30), pady=2)
    Button(integrityRightFrame, text='Kontrola súdržnosti', command=integrity).pack(padx=10, pady=10)

    # views
    Button(viewFrame, text=ResponseView.name().upper(), command=responseview)\
        .pack(expand=True, side=LEFT, padx=10, pady=10)
    Button(viewFrame, text=SplinterView.name().upper(), command=splinterview)\
        .pack(expand=True, side=LEFT, padx=10, pady=10)
    Button(viewFrame, text=Overview.name().upper(), command=overview)\
        .pack(expand=True, side=LEFT, padx=10, pady=10)

    mw.mainloop()
