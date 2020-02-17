from collections import defaultdict, OrderedDict
from model import SplinterView, NamingUnitTable, ImageTable, SourceWordTable, SplinterTable, Overview, Table
import configuration


class SyncManager:

    __RULES = defaultdict(tuple)
    __RULES[SplinterView] = (NamingUnitTable, SplinterTable)
    __RULES[NamingUnitTable] = (SplinterView,)
    __RULES[ImageTable] = (SplinterView,)
    __RULES[SourceWordTable] = (SplinterView,)
    __RULES[SplinterTable] = (SplinterView,)

    def __init__(self, classes, *args):

        # argumenty pre instanciaciu
        self.__args = args

        # povodne triedy
        self.__classes = classes

        # instancie vytvorene z povodnych tried
        self.__objs = [cls(*args) for cls in classes]

        # triedy, ktore boli zosynchronizovane a boli zmenene
        self.__modified = []

        # triedy, ktore boli zosynchronizovane, ale neboli zmenene
        self.__stayed = []

    @property
    def __touched(self) -> set:
        """
        Vrati mnozinu tried, ktorymi sme sa uz zaoberali.
        Sluzi na to, aby sa nespustala sync na jeden object viackrat.
        """
        return set(self.__modified) | set(self.__stayed)

    def __sync(self, objs, unhighlight):
        """Zosynchronizuje dane instancie a tiez rekurzivne podla pravidiel."""
        if len(objs) > 0:

            # zoznam tried na rekurziu
            affected = []

            for obj in objs:
                if not obj.sheet_created:
                    continue
                else:
                    modified = obj.sync(unhighlight)
                    if configuration.DEBUG:
                        print('Modified:', 'YES' if modified else 'NO')
                    if modified:
                        self.__modified.append(obj.__class__)
                        potential = list(self.__RULES[obj.__class__])

                        # ak je `obj` instanciou Table, chceme zosynchronizovat Overview
                        if configuration.SYNC_OVERVIEW and isinstance(obj, Table) and Overview not in potential:
                            potential.append(Overview)

                        # pridat do dalsieho kola triedy, na ktore ma vplyv `obj`
                        # a este sme sa ich nepokusali synchronizovat
                        affected.extend(cls for cls in potential if cls not in self.__touched)
                    else:
                        self.__stayed.append(obj.__class__)
            self.__sync([cls(*self.__args, as_affected=True) for cls in affected], False)

    def generate(self, unhighlight, **kwargs):
        """Spusti synchronizaciu a generovanie."""
        for obj in self.__objs:
            obj.sync(unhighlight)
            obj.generate(**kwargs)
        self.sync(False)

    def integrity(self, unhighlight) -> OrderedDict:
        """Spusti synchronizovanie a kontrolu integrity."""
        result = OrderedDict()
        for obj in self.__objs:
            obj.sync(unhighlight)
            obj.integrity_before()
            result[obj.name()] = (obj.integrity_add(), obj.integrity_junk())
        self.sync(False)
        return result

    def sync(self, unhighlight):
        self.__sync(self.__objs, unhighlight)

    @property
    def modified(self):
        """Zoznam povodnych tried, ktore boli zmenene pri synchronizacii."""
        return [cls for cls in self.__classes if cls in self.__modified]

    @property
    def stayed(self):
        """Zoznam povodnych tried, ktore pri synchronizacii ostali nezmenene."""
        return [cls for cls in self.__classes if cls in self.__stayed]

    @property
    def affected(self):
        """Zoznam tried, ktore boli zmenene v dosledku synchronizacie inej triedy."""
        return [cls for cls in self.__modified if cls not in self.__classes]
