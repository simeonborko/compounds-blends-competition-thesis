class SplinterManager:
    """
    Splinter Manager uchovava vytvorene Splinter objekty, aby sa nemuseli vytvarat znova.
    Hlavny vyznam je v tom, aby sa Splinter.__all_alignments nepocitalo znova, pretoze to trva dlho.
    """

    def __init__(self):
        self.__data = {}

    def get(self, SplinterCls, naming_unit: str, source_word: str, strict: bool):
        key = (SplinterCls, naming_unit, source_word, strict)
        if key in self.__data:
            # print('hit')
            return self.__data[key]
        splinter = SplinterCls(naming_unit, source_word, strict)
        self.__data[key] = splinter
        # print('miss')
        return splinter

    def clear(self):
        self.__data.clear()
