from collections import defaultdict

from model import SplinterView, NamingUnitTable, ImageTable, SourceWordTable, SplinterTable


class DependencyManager:

    __EFFECT_DICT = defaultdict(tuple)
    __EFFECT_DICT[SplinterView] = (NamingUnitTable, ImageTable, SourceWordTable, SplinterTable)
    __EFFECT_DICT[NamingUnitTable] = (SplinterView,)
    __EFFECT_DICT[ImageTable] = (SplinterView,)
    __EFFECT_DICT[SourceWordTable] = (SplinterView,)
    __EFFECT_DICT[SplinterTable] = (SplinterView,)

    def __init__(self):
        self.__synced = defaultdict(lambda: False)

    def set_synced(self, tablecls):
        self.__synced[tablecls] = True

    @property
    def effected(self):
        ef = []
        for k, v in self.__EFFECT_DICT.items():
            if self.__synced[k]:
                ef.extend(cls for cls in v if self.__synced[cls] is False)
        return ef
