from enum import Enum, auto
from typing import Tuple, Optional


def create_matrix(sw1, sw2):
    """
    Vytvori maticu zhodnych znakov pre sw1 a sw2.
    Vysledok pre slova mrak (sw1) a kengura (sw2):
       K  E  N  G  U  R  A
    K  1  .  .  .  .  .  .
    A  .  .  .  .  .  .  1
    R  .  .  .  .  .  1  .
    M  .  .  .  .  .  .  .
    """
    return tuple(
        tuple(sw1_item == sw2_item for sw2_item in sw2)
        for sw1_item in reversed(sw1)
    )


def print_matrix(matrix):
    for row in matrix:
        print(*('1' if item else '.' for item in row))


def matrix_to_diamond(matrix) -> (tuple, tuple):
    """
    Prevod matice na diamant. Diagonaly matice su riadky diamantu.
    Priklad:
    Matica:
        . . . . . .
        . . . . 1 .
        . . . 1 . .
        . 1 . . . .
        1 . . . . .
    Diamant:
        .
        . .
        . . .
        . . . .
        1 1 . . .
        . . 1 1 .
        . . . .
        . . .
        . .
        .
    """
    matrix_rows = len(matrix)
    matrix_cols = len(matrix[0])
    diamond_rows = matrix_rows + matrix_cols - 1
    diamond = []
    diamond_to_matrix = []
    for drow in range(diamond_rows):
        mrow = min(drow, matrix_rows - 1)
        mcol = drow - mrow
        items = []
        indices_items = []
        while mrow >= 0 and mcol < matrix_cols:
            items.append(matrix[mrow][mcol])
            indices_items.append((mrow, mcol))
            mrow -= 1
            mcol += 1
        diamond.append(tuple(items))
        diamond_to_matrix.append(tuple(indices_items))
    return tuple(diamond), tuple(diamond_to_matrix)


def print_diamond(diamond):
    for row in diamond:
        print(*('1' if item else '.' for item in row))


class DiamondLinePosition(Enum):
    MIDDLE = auto()
    LEFT = auto()
    RIGHT = auto()
    BOTH = auto()
    NONE = auto()


def position_in_diamond_line(line) -> (DiamondLinePosition, int, int):
    """
    Najde poziciu prvej zhody v riadku diamantu.
    Vyhladava sa od stredu.
    Vrati tri hodnoty: DiamondLinePosition, lavy kurzor (index), pravy kurzor (index)
    """
    rcur = len(line) // 2
    lcur = rcur if len(line) % 2 else rcur - 1

    if rcur == lcur and line[lcur]:
        return DiamondLinePosition.MIDDLE, lcur, rcur

    left_hit = False
    right_hit = False

    while lcur >= 0:
        left_hit = line[lcur]
        if left_hit:
            break
        lcur -= 1
    while rcur < len(line):
        right_hit = line[rcur]
        if right_hit:
            break
        rcur += 1

    if left_hit and right_hit:
        position = DiamondLinePosition.BOTH
    elif left_hit:
        position = DiamondLinePosition.LEFT
    elif right_hit:
        position = DiamondLinePosition.RIGHT
    else:
        position = DiamondLinePosition.NONE

    return position, lcur, rcur


def sequence_in_diamond_line(line, pos: DiamondLinePosition, lcur: int, rcur: int) -> Optional[Tuple[int, int]]:
    if pos == DiamondLinePosition.NONE:
        return None

    lseqcur = None
    rseqcur = None

    if pos in (DiamondLinePosition.LEFT, DiamondLinePosition.MIDDLE, DiamondLinePosition.BOTH):
        lseqcur = lcur
        while lseqcur > 0 and line[lseqcur - 1]:
            lseqcur -= 1

    if pos in (DiamondLinePosition.RIGHT, DiamondLinePosition.MIDDLE, DiamondLinePosition.BOTH):
        rseqcur = rcur
        while rseqcur < len(line) - 1 and line[rseqcur + 1]:
            rseqcur += 1

    if pos == DiamondLinePosition.BOTH:
        left_seq_length = lcur - lseqcur + 1
        right_seq_length = rseqcur - rcur + 1
        pos = DiamondLinePosition.LEFT if left_seq_length >= right_seq_length else DiamondLinePosition.RIGHT

    if pos == DiamondLinePosition.LEFT:
        return lseqcur, lcur
    elif pos == DiamondLinePosition.RIGHT:
        return rcur, rseqcur
    elif pos == DiamondLinePosition.MIDDLE:
        return lseqcur, rseqcur
    else:
        raise Exception("Unknown position in overlapable.py")


def levels_from_sequence(line_idx: int, seq: Tuple[int, int], diamond_to_matrix) -> (int, int):
    """
    Ziska level pre SW1 a level pre SW2.
    """
    # pre sw1 sa berie koniec sekvencie, cize seq[1]
    sw1_level = diamond_to_matrix[line_idx][seq[1]][0]
    # pre sw2 sa berie zaciatok sekvencie, cize seq[0]
    sw2_level = diamond_to_matrix[line_idx][seq[0]][1]
    return sw1_level, sw2_level


def get_overlapable(sw1, sw2) -> Optional[Tuple[int, int, int]]:
    matrix = create_matrix(sw1, sw2)
    diamond, diamond_to_matrix = matrix_to_diamond(matrix)
    seq = None
    for d_idx, d_line in enumerate(diamond):
        pos = position_in_diamond_line(d_line)
        seq = sequence_in_diamond_line(d_line, *pos)
        if seq is not None:
            levels = levels_from_sequence(d_idx, seq, diamond_to_matrix)
            return seq[1] - seq[0] + 1, levels[0], levels[1]
    return None


if __name__ == '__main__':
    matrix = create_matrix('XYABZ', 'XY?AB ')
    print_matrix(matrix)
    print()
    diamond, _ = matrix_to_diamond(matrix)
    print_diamond(diamond)

    print()

    pos_4 = position_in_diamond_line(diamond[4])
    pos_5 = position_in_diamond_line(diamond[5])
    print(pos_4)
    print(pos_5)

    seq_4 = sequence_in_diamond_line(diamond[4], *pos_4)
    seq_5 = sequence_in_diamond_line(diamond[5], *pos_5)
    print(seq_4)
    print(seq_5)

    print(get_overlapable('XYABZ', 'XY?AB '))
