import json
from os.path import isfile


class ListSaver:

    def __init__(self, filename: str, default_data: list):
        self.__filename = filename
        self.__data = default_data

    def __same_length(self, other: list) -> bool:
        return len(self.__data) == len(other)

    def __same_value_types(self, other: list) -> bool:
        return set(type(v) for v in self.__data) == set(type(v) for v in other)

    def __enter__(self):
        if isfile(self.__filename):
            with open(self.__filename) as fp:
                loaded = json.load(fp)
            if not self.__same_length(loaded) or not self.__same_value_types(loaded):
                raise Exception('Nespravne data v subore {}'.format(self.__filename))
            self.__data = loaded
        self.__modified = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__modified:
            with open(self.__filename, 'w') as fp:
                json.dump(self.__data, fp)

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        if self.__data[key] != value:
            self.__data[key] = value
            self.__modified = True

    def __iter__(self):
        return iter(self.__data)
