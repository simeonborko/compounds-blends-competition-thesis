from typing import Union


class Entity:

    _ALLOWED = None
    _PRIMARY = None

    def __init__(self, data: dict):
        self.__data = data
        self.__modified = False

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        if key in self._PRIMARY:
            raise Exception('Hodnota v stlpci patriacom do primarneho kluca nemoze byt zmenena')
        if self.__data[key] != value:
            self.__data[key] = value
            self.__modified = True

    def get_data(self) -> Union[dict, None]:
        return {k: v for k, v in self.__data.items() if k[:2] == 'G_' or k in self._ALLOWED} if self.__modified else None
