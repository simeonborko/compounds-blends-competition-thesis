from unidecode import unidecode


class Letters:

    CONSONANTS = ('d', 't', 'n', 'l', 'ch', 'h', 'g', 'k', 'c', 'dz', 'j', 'm', 'b', 'p', 'v', 'z', 's', 'f', 'r')
    VOWELS = ('a', 'e', 'i', 'o', 'u', 'y')
    DIPHTHONGS = ('ia', 'ie', 'iu', 'ô')

    @classmethod
    def get_type(cls, letter: str) -> str:

        if letter in cls.DIPHTHONGS:
            return 'd'  # diphthong

        letter = unidecode(letter)

        if letter in cls.CONSONANTS:
            return 'c'  # consonant

        elif letter in cls.VOWELS:
            return 'v'  # vowel

        else:
            return 'o'  # other
