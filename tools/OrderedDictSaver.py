import json
from collections import OrderedDict
from os.path import isfile


class OrderedDictSaver:

    def __init__(self, filename, default_data):
        self.__filename = filename
        self.__data = default_data

    def __same_keys(self, other: OrderedDict) -> bool:
        return set(self.__data.keys()) == set(other.keys())

    def __same_value_types(self, other: OrderedDict) -> bool:
        return set(type(v) for v in self.__data.values()) == set(type(v) for v in other.values())

    def __enter__(self):
        if isfile(self.__filename):
            with open(self.__filename) as fp:
                loaded = OrderedDict(json.load(fp))
            if not self.__same_keys(loaded) or not self.__same_value_types(loaded):
                raise Exception('Nespravne data v subore {}'.format(self.__filename))
            self.__data = loaded
        self.__modified = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__modified:
            with open(self.__filename, 'w') as fp:
                json.dump(list(self.__data.items()), fp)

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        if self.__data[key] != value:
            self.__data[key] = value
            self.__modified = True

    def items(self):
        return self.__data.items()
