from functools import reduce
from typing import List


def __remove_stress_and_hyphen(expr):
    """
    Rozdeli vyraz na slova a prizvuky a spojovniky prevedie na bodky (zlomy slabik).
    :param expr: Retazec (moze byt aj prazdny).
    :return: Zoznam slov bez prizvukov a spojovnikov (nahradene bodkami) bez prazdnych retazcov.
    """

    def __remove_from_word(word):
        """
        Odstrani prizvuk na zaciatku a prevedie prizvuky a spojovniky na bodky (zlomy slabik).
        :param word: Slovo s prizvukmi a spojovnikmi, nesmie byt prazdny retazec!
        :return: Slovo bez prizvukov a spojovnikov.
        """
        stress = ('ˈ', 'ˌ')
        # odstranenie prizvuku na zaciatku
        if word[0] in stress:
            word = word[1:]
        return word.replace(stress[0], '.').replace(stress[1], '.').replace('-', '.')

    return [__remove_from_word(word) for word in expr.split(' ') if word != '']


def count_syllables(phonetic):
    """
    Ziska pocet slabik.
    :param phonetic: Retazec (moze obsahovat medzery).
    :return: Pocet slabik alebo None ak phonetic nie je string.
    """
    if type(phonetic) is not str:
        return None
    return sum([word.count('.')+1 for word in __remove_stress_and_hyphen(phonetic)])


def remove_syllable_division(phonetic):
    """
    Odstrani rozdelenie slabik (prizvuky a bodky).
    :param phonetic: Retazec (moze obsahovat medzery).
    :return: Zoznam slov bez rozdelenia slabik (bez prazdnych retazcov).
    """
    return [word.replace('.', '') for word in __remove_stress_and_hyphen(phonetic)]


def get_syllables(phonetic) -> List[str]:
    """
    Rozdeli foneticky prepis na slabiky.
    :param phonetic: Retazec (moze obsahovat medzery).
    :return: Zoznam slabik, pricom slabika je retazec.
    """

    # zoznam slov, slovo - zoznam slabik, slabika - retazec hlasok
    words = [word.split('.') for word in __remove_stress_and_hyphen(phonetic)]

    # zoznam slabik celeho vyrazu, slabika - retazec hlasok
    syllables = reduce((lambda x, y: x + y), words)

    return syllables
