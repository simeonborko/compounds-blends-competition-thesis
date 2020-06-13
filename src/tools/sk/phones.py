import re

phones_excluding_dzdz = (
    'I_\\^U\\\\',
    'I_\\^a',
    'I_\\^E',
    'U_\\^O',
    'U_\\^',
    'I_\\^',
    'r\\=\\:',
    'l\\=\\:',
    'a\\:',
    'E\\:',
    'I\\:',
    'O\\:',
    'U\\:',
    'J\\\\',
    'ts',
    'tS',
    'h\\\\',
    'r\\=',
    'l\\=',
    'a',
    'E',
    'I',
    'O',
    'U',
    '\\{',
    'p',
    'b',
    't',
    'd',
    'c',
    'k',
    'g',
    'f',
    'v',
    'w',
    's',
    'z',
    'S',
    'Z',
    'x',
    'G',
    'j',
    'r',
    'l',
    'L',
    'm',
    'F',
    'n',
    'N',
    'J'
)

PHONES_PATTERN_EXCLUDING_DZDZ = re.compile('|'.join(phones_excluding_dzdz))

phones = (
    'dz',
    'dZ',
) + phones_excluding_dzdz

PHONES_PATTERN = re.compile('|'.join(phones))
