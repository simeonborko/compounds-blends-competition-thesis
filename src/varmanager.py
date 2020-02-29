import json
from collections import OrderedDict
from genericpath import isfile
from tkinter import IntVar


class VarManager:

    def __init__(self, filename):
        self.__filename = filename
        self.__groups = OrderedDict()
        self.__loaded = None

    def __enter__(self):
        if isfile(self.__filename):
            with open(self.__filename) as fp:
                self.__loaded = json.load(fp)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any(group.modified for group in self.__groups.values()):
            data = [group.data for group in self.__groups.values()]
            with open(self.__filename, 'w') as fp:
                json.dump(data, fp)

    def __getitem__(self, item):
        return self.__groups[item]

    def group(self, name):
        if name in self.__groups:
            raise Exception
        if self.__loaded:
            g = VarGroup(name, self.__loaded.pop(0))
        else:
            g = VarGroup(name)
        self.__groups[name] = g
        return g


class VarGroup:

    def __init__(self, name, loaded=None):
        self.__name = name
        self.__loaded = loaded
        self.__initvals = []
        self.__vars = []

    def __iter__(self):
        return iter(self.checked)

    def __getitem__(self, item) -> bool:
        return bool(self.__vars[item].get())

    def var(self) -> IntVar:
        value = self.__loaded.pop(0) if self.__loaded else 1
        var = IntVar(value=value)
        self.__initvals.append(value)
        self.__vars.append(var)
        return var

    @property
    def modified(self) -> bool:
        return any(val != var.get() for val, var in zip(self.__initvals, self.__vars))

    @property
    def data(self) -> list:
        return [var.get() for var in self.__vars]

    @property
    def checked(self) -> list:
        return [i for i, var in enumerate(self.__vars) if var.get() == 1]
