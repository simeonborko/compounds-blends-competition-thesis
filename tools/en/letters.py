from tools.redundant import REDUNDANT


def remove_redundant(word):
    """Odstrani symboly, ktore robia problemy pri pocitani"""
    word = word.strip()
    for r in REDUNDANT:
        word = word.replace(r, '')
    return word


def count_letters(expr: str) -> int:
    return len(get_letters_list(expr))


def get_letters_list(expr: str) -> list:
    return list(remove_redundant(expr))
