from unidecode import unidecode
from sys import stderr
from .phones import PHONES_PATTERN
from enum import Enum

REDUNDANT = ' -–,.!"()'


def replace_i(word):
    return word.replace('ɪ', 'I')


def remove_redundant(word):
    word = word.strip()
    for r in REDUNDANT:
        word = word.replace(r, '')
    return word


def decapitalize(phrase):
    src = phrase.split(' ')
    words = []
    for word in src:
        if word:
            word = word[0].lower() + word[1:]
        words.append(word)
    return ' '.join(words)


def count_letters(word, chdzdz=True):
    """Count letters. """
    prev = None
    count = 0

    for letter in remove_redundant(word.lower()):
        if chdzdz:
            if prev == 'c' and letter == 'h' or prev == 'd' and letter in ('z', 'ž'):
                prev = letter
                continue
        count += 1
        prev = letter
    return count


def get_phones_list(word):
    """Get phones list."""
    lst = PHONES_PATTERN.findall(remove_redundant(word))

    # Check if ok
    cnt = 0
    for letter in lst:
        cnt += len(letter)
    if cnt != count_letters(word, False):
        raise Exception(word, lst, len(word), cnt)

    return lst


def count_phones(word):
    """Count phones in word in phonetic transcription."""
    try:
        lst = get_phones_list(word)
    except Exception as e:
        if word[0] != word[0].lower():
            return count_phones(decapitalize(word))
        #print(e, file=stderr)
        return '!!!'
    return len(lst)


class SplinterType(Enum):
    GRAPHIC = 1
    PHONETIC = 2
    SYLLABIC = 3


class Splinter:
    """
    _name - Naming Unit
    _sw - Source word
    strict, soft - Result from _align_words
    accent_flag - If it is necessary to use soft alignment to achieve such splinter.
    """
    def __init__(self, name, sw, type):

        # Set name, orig_name and sw
        if type is SplinterType.GRAPHIC:
            self._orig_name = name.strip()
            self._name = self._orig_name.lower()
            self._sw = sw.strip().lower()
        elif type is SplinterType.PHONETIC:
            self._name = self._orig_name = name.strip()
            self._sw = sw.strip()
        elif type is SplinterType.SYLLABIC:
            self._orig_name = name
            self._name = [x.lower() for x in name]
            self._sw = [x.lower() for x in sw]
        else:
            raise Exception

        self.accent_flag = False
        self._type = type

        self._get_aligns()

    @staticmethod
    def _ign_graphic(foo):
        return unidecode(foo).replace('y', 'i')

    @staticmethod
    def _ign_phonetic(foo):
        return foo.replace(':', '')

    @classmethod
    def _ign_syllabic(cls, foo):
        return [cls._ign_graphic(x) for x in foo]

    def _get_aligns(self):

        self.strict = Alignment(self._name, self._sw, self._type, self._orig_name)

        if self._type is SplinterType.GRAPHIC:
            name = self._ign_graphic(self._name)
            sw = self._ign_graphic(self._sw)
            self.soft = Alignment(name, sw, self._type, self._orig_name)

        elif self._type is SplinterType.PHONETIC:
            name = self._ign_phonetic(self._name)
            sw = self._ign_phonetic(self._sw)
            self.soft = Alignment(name, sw, self._type, name)

        elif self._type is SplinterType.SYLLABIC:
            name = self._ign_syllabic(self._name)
            sw = self._ign_syllabic(self._sw)
            self.soft = Alignment(name, sw, self._type, self._orig_name)

        else:
            raise Exception

        if self.strict != self.soft and self.strict.length != self.soft.length:
            self.accent_flag = True


class Alignment:

    length = 0
    a_idx = None
    b_idx = None

    def __init__(self, name, sw, type, original_name):
        self._name = name
        self._sw = sw
        self._type = type
        self._original_name = original_name

        self._get_align(name, sw)
        self._get_word()

    def get_segment_range(self) -> range:
        return range(self.a_idx, self.a_idx + self.length)

    def _get_align(self, name, sw):
        for a_counter, a_letter in enumerate(name):
            for b_counter, b_letter in enumerate(sw):
                match = 0
                remain_a = len(name) - a_counter
                remain_b = len(sw) - b_counter
                for i in range(min(remain_a, remain_b)):
                    if name[a_counter + i] != sw[b_counter + i]:
                        break
                    match += 1
                if self.length < match:
                    self.length = match
                    self.a_idx = a_counter
                    self.b_idx = b_counter

    def _get_word(self):
        start = self.a_idx
        length = self.length
        if start is None or length is None:
            raise Exception('Cannot find splinter', self._name, self._sw)
        stop = start + length
        self._word = self._original_name[start:stop]

    def get_length(self):
        if self._type == SplinterType.GRAPHIC:
            return count_letters(self._word)
        elif self._type == SplinterType.PHONETIC:
            return count_phones(self._word)
        elif self._type == SplinterType.SYLLABIC:
            return len(self._word)
        else:
            raise Exception

    def get_shortening_type(self):

        if count_letters(self._sw) == self.get_length():
            return 'FSW'
        elif self.b_idx == 0:
            return 'RS'
        elif self.b_idx + self.length == len(self._sw):
            return 'LS'

        return None

    def get_sw_idx(self):
        if self.b_idx is None:
            raise Exception('Index of source word in Alignment is not set')
        return self.b_idx

    def __str__(self):
        if self._type == SplinterType.SYLLABIC:
            return '-'.join(self._word)
        return self._word


def get_placement(shortening, source_word, syllabification, offset, length):

    names = {
        'NC': 'nucleus-coda',
        'S': 'syllable',
        'ON': 'onset-nucleus'
    }

    def get_map(syllables):
        map = []
        for i, syllable in enumerate(syllables):
            for j in range(len(syllable)):
                map.append(i)
        return map

    def is_vowel(letter):
        vowels = ('a', 'e', 'i', 'o', 'u', 'y')
        return unidecode(letter.lower()) in vowels

    def analyze_pair(a, b, first_vowel_allowed=True, second_vowel_allowed=True):
        if first_vowel_allowed and is_vowel(a) and not is_vowel(b):
            return names['NC']
        elif second_vowel_allowed and not is_vowel(a) and is_vowel(b):
            return names['ON']
        else:
            raise Exception('Analyze pair failed', a, b)

    def analyze_syllable(syllable, letter_idx):
        length = len(syllable)

        if length == 2:
            if letter_idx == 0:
                return analyze_pair(syllable[0], syllable[1])
            else:
                raise Exception('Analyze syllable failed', syllable, letter_idx)

        elif length == 3:
            if letter_idx == 0:
                return analyze_pair(syllable[0], syllable[1], first_vowel_allowed=False)
            elif letter_idx == 1:
                return analyze_pair(syllable[1], syllable[2], second_vowel_allowed=False)
            else:
                raise Exception('Analyze syllable failed', syllable, letter_idx)

        else:
            raise Exception('Bad length of syllable')

    def get_before_count(syllables, syllable_idx):
        bc = 0
        for syllable in syllables[:syllable_idx]:
            bc += len(syllable)
        return bc

    if source_word.find(' ') != -1:
        raise Exception('Word contains space')

    syllables = syllabification.split('-')
    map = get_map(syllables)

    if shortening == 'RS' and offset == 0 and length >= 2:
        left = map[length - 1]
        right = map[length]
        if left != right:
            return names['S']  # syllable
        else:
            before_count = get_before_count(syllables, left)
            return analyze_syllable(syllables[left], length - before_count - 1)
    elif shortening == 'LS' and offset > 0:
        left = map[offset - 1]
        right = map[offset]
        if left != right:
            return names['S']
        else:
            before_count = get_before_count(syllables, left)
            return analyze_syllable(syllables[left], offset - before_count - 1)

    else:
        raise Exception('Cannot determine')


def get_placement_or_none(*args):
    try:
        return get_placement(*args)
    except Exception as e:
        print(e, file=stderr)


class SegmentCounter:

    def __init__(self, splinters: list):
        self.strict_segs = [0] * len(splinters[0]._name)
        self.soft_segs = [0] * len(splinters[0]._name)
        for s in splinters:
            for i in s.strict.get_segment_range():
                self.strict_segs[i] += 1
            for i in s.soft.get_segment_range():
                self.soft_segs[i] += 1

    def overlap_numbers(self) -> (int, int):
        """Vracia strict, soft"""
        return sum(x > 1 for x in self.strict_segs), sum(x > 1 for x in self.soft_segs)
