from os.path import isfile

from openpyxl import load_workbook

from src import configuration
from src.model import NamingUnitTable
from src.syncmanager import SyncManager
from src.tools import Connection
from src.worker import backup


def generate_naming_unit(unhighlight=True, force=True):
    if not isfile(configuration.XLSX_FILE):
        raise Exception('Chyba', 'Súbor {} neexistuje'.format(configuration.XLSX_FILE))
    backup()

    wb = load_workbook(configuration.XLSX_FILE)
    with Connection() as conn:
        syncmanager = SyncManager([NamingUnitTable], wb, conn)
        syncmanager.generate(unhighlight, force=force)
        conn.commit()

    wb.save(configuration.XLSX_FILE)


if __name__ == '__main__':
    generate_naming_unit()
