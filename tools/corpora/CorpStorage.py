import json
from pathlib import Path
from typing import Dict, Set, List, Union, Optional
from datetime import datetime

import configuration as conf
from tools import CorpConnection


DataDict = Dict[str, Optional[int]]


class CorpStorage:

    def __init__(self, tblname: str):
        self._tblname = tblname
        self._data: DataDict = {}
        self._touched: Set[str] = set()

    def load(self):
        with CorpConnection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT word, freq FROM {}".format(self._tblname))
            self._data.update(cur)

    def save(self):

        if len(self._touched) == 0:
            return

        # data_to_save: List[Tuple[str, Optional[int]]] = [(word, self._data[word]) for word in self._touched]

        # noinspection PyBroadException
        try:

            query = "INSERT INTO {} (word, freq) VALUES {}".format(
                self._tblname,
                ', '.join('(%s, %s)' for _ in range(len(self._touched)))
            )
            params: List[Union[str, Optional[int]]] = []
            for word in self._touched:
                params.append(word)
                params.append(self._data[word])

            with CorpConnection() as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                conn.commit()

        except Exception:
            dirpath = Path(conf.CORPORA_BACKUP_DIR)
            filepath = dirpath / '{}-{}.json'.format(
                datetime.now().strftime('%Y_%m_%d-%H_%M_%S'),
                str(self._tblname)
            )

            with filepath.open('w') as fp:
                json.dump({'data': self._data, 'touched': list(self._touched)}, fp)

            raise

    def __getitem__(self, item):
        val = self._data[item]
        return val if val != -1 else None

    def __setitem__(self, key, value):
        self._data[key] = value
        self._touched.add(key)

    def __contains__(self, item):
        return item in self._data

    def set_as_faulty(self, item):
        self[item] = -1

    # @property
    # def data(self) -> DataDict:
    #     return self._data.copy()
    #
    # def set_many(self, data: DataDict):
    #     self._data.update(data)
    #     self._touched.update(data.keys())

    @property
    def data_keys(self) -> Set[str]:
        return set(self._data.keys())
