from .phones import get_phones_list
from .syllables import get_syllables


def get_interfaces(phonetic) -> list:
    """
    Ziska rozhrania slabik.
    Priklad: 0 1 | 2 3 4 | 5 6 => [(0, 1), (4, 5)]
    :param phonetic: Retazec (moze obsahovat medzery).
    :return: Zoznam rozhrani. Rozhranie je dvojica indexov.
    """
    interfaces = []
    syll_list = [get_phones_list(syll) for syll in get_syllables(phonetic)]

    counter = -1

    for syll_idx in range(len(syll_list) - 1):

        counter += len(syll_list[syll_idx])
        interfaces.append((counter, counter + 1))

    return interfaces
