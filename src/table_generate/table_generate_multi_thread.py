import sys
import threading
from queue import Queue
from time import sleep

from src import configuration


# noinspection PyProtectedMember
def updater(table, q: Queue, thread_info: dict):
    while True:
        sleep(10)

        # zistovanie putting_done musi byt pred ziskavanim velkosti fronty
        putting_done = thread_info['putting_done']
        size = q.qsize()
        args = []

        for _ in range(size):
            args.append(q.get())

        if len(args):
            query = "UPDATE {} SET {} WHERE {}".format(
                table.name(),
                ", ".join("{0}=%({0})s".format(g) for g in table.generated_fields),
                " AND ".join("{0}=%({0})s".format(p) for p in table.primary_fields)
            )
            thread_info['affected'] += table._executemany(query, args).result or 0

        else:
            # ak sa nic neaktualizuje, tak aspon pingneme, aby nas server neodpojil
            table._ping_connection()

        for _ in range(size):
            q.task_done()

        if putting_done:
            return


def multi_thread(table, cursor, cls) -> int:
    q = Queue()
    thread_data = {
        'putting_done': False,
        'affected': 0
    }
    t = threading.Thread(target=updater, args=(table, q, thread_data))
    t.start()

    try:

        entity_modified_counter = 0

        for data in cursor:
            entity = cls(table, data)
            entity.generate()
            if entity.modified:
                q.put(entity.data)
                entity_modified_counter += 1

    finally:

        # ukoncujuca podmienka vlakna musi byt tu, vo finally, aby sa to ukoncilo vzdy
        thread_data['putting_done'] = True

        q.join()

        # pockame max 10 minut, viac to asi nema zmysel
        t.join(10 * 60)
        if t.is_alive():
            raise Exception('Vlakno na aktualizaciu databazy sa zaseklo')

    if entity_modified_counter != thread_data['affected']:
        if configuration.DEBUG:
            print("Pocet args: {}, pocet affected: {}".format(entity_modified_counter, thread_data['affected']),
                  file=sys.stderr)

    return thread_data['affected']
