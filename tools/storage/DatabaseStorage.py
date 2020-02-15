import json
from datetime import datetime
from pathlib import Path
from typing import Set, List, Union, Optional


class DatabaseStorage:

    def __init__(self, tblname: str, key_field: str, value_field: str, backup_dir: str, connection_cls, faulty_value):
        self._tblname = tblname
        self._key_field = key_field
        self._value_field = value_field
        self._backup_dir = backup_dir
        self._connection_cls = connection_cls
        self._faulty_value = faulty_value
        self._data: dict = {}
        self._touched: Set[str] = set()

    def load(self):
        with self._connection_cls() as conn:
            cur = conn.cursor()
            cur.execute("SELECT {}, {} FROM {}".format(self._key_field, self._value_field, self._tblname))
            self._data.update(cur)

    def save(self):

        if len(self._touched) == 0:
            return

        # data_to_save: List[Tuple[str, Optional[int]]] = [(word, self._data[word]) for word in self._touched]

        # noinspection PyBroadException
        try:

            query = "INSERT INTO {} ({}, {}) VALUES {}".format(
                self._tblname,
                self._key_field, self._value_field,
                ', '.join('(%s, %s)' for _ in range(len(self._touched)))
            )
            params: List[Union[str, Optional[int]]] = []
            for word in self._touched:
                params.append(word)
                params.append(self._data[word])

            with self._connection_cls() as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                conn.commit()

        except Exception:
            dirpath = Path(self._backup_dir)
            dirpath.mkdir(parents=True, exist_ok=True)
            filepath = dirpath / '{}-{}.json'.format(
                datetime.now().strftime('%Y_%m_%d-%H_%M_%S'),
                str(self._tblname)
            )

            with filepath.open('w') as fp:
                json.dump({'data': self._data, 'touched': list(self._touched)}, fp)

            raise

    def __getitem__(self, item):
        val = self._data[item]
        return val if val != self._faulty_value else None

    def __setitem__(self, key, value):
        self._data[key] = value
        self._touched.add(key)

    def __contains__(self, item):
        return item in self._data

    def set_as_faulty(self, item):
        self[item] = self._faulty_value

    @property
    def data_keys(self) -> Set[str]:
        return set(self._data.keys())
