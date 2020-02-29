"""Pozor, databaza vracia bytes! V tomto subore nepouzivam funkciu decoded"""

from openpyxl import load_workbook
import csv
from src.tools.tools import Connection, tsv_reader, get_res2lang, decoded, Table
from collections import OrderedDict


def reader(wb, sheet_name):
    rows = wb[sheet_name].rows
    return map(lambda r: [c.value for c in r], rows)


def participant_info():
    """Nastavi jazyk a pohlavie tam, kde nie su"""
    wb = load_workbook('data/1 SK overview doplnené o objekty.xlsx', read_only=True)
    rows = reader(wb, 'Participant Info')
    # 0 ID
    # 1 Language 1
    # 2 Year of birth
    # 3 Age
    # 4 Sex
    # 5 Occupation
    # 6 Country
    # 7 Education
    # 8 Language 2
    # 9 Language 3
    next(rows)

    cursor = conn.cursor()

    for row in rows:

        cursor.execute(
            'UPDATE respondent SET first_language = %s WHERE respondent_id = %s AND first_language is null',
            (row[1], row[0])
        )
        cursor.execute(
            'UPDATE respondent SET sex = %s WHERE respondent_id = %s AND sex is null',
            (row[4], row[0])
        )


def check_responses(conn, rows, filename):
    # kontrola, ci lydka neupravila Naming Unit
    with open('data/export/'+filename, 'w') as outf:
        writer = csv.writer(outf, delimiter='\t')
        writer.writerow(('id', 'respondent_id', 'image_id', 'naming_unit', 'DB naming_unit'))
        c = conn.cursor()
        for r in rows:
            response_id = r[0].strip()
            respondent_id = r[1].strip()
            image_id = r[5].strip()
            naming_unit = r[12].strip()

            # je nieco take aj v databaze?
            c.execute(
                'SELECT COUNT(*) FROM response WHERE respondent_id = %s AND image_id = %s AND naming_unit = %s',
                (respondent_id, image_id, naming_unit)
            )

            # ak ano, pokracuj
            if c.fetchone()[0] == 1:
                continue

            # ak nie, zisti, co mame v db

            c.execute(
                'SELECT naming_unit FROM response WHERE respondent_id = %s AND image_id = %s LIMIT 1',
                (respondent_id, image_id)
            )

            d_naming_unit = next(decoded(c))[0]

            if naming_unit != d_naming_unit:
                writer.writerow((
                    response_id,
                    respondent_id,
                    image_id,
                    naming_unit,
                    d_naming_unit
                ))


def import_naming_units(conn, rows, filename):

    c = conn.cursor()

    # respondent_id => (first_language, survey_language)
    res2lang = get_res2lang(c)

    # mnozina dvojic (image_id, naming_unit)
    # conflicts = set()

    # (naming_unit, first_language, survey_language, image_id) => OrderedDict
    # data = OrderedDict()

    data = []

    kfields = ('nu_graphic', 'first_language', 'survey_language', 'image_id')
    vfields = ('nu_phonetic', 'nu_word_class', 'nu_syllabic', 'nu_graphic_len', 'nu_phonetic_len', 'nu_syllabic_len',
               'n_of_overlapping_letters', 'n_of_overlapping_phones', 'sw1_graphic', 'sw2_graphic', 'sw3_graphic',
               'wf_process', 'lexsh_main', 'lexsh_sm', 'lexsh_whatm', 'split_point_1', 'split_point_2')

    table = Table(kfields, vfields)

    for r in rows:

        """naming_unit
first_language
survey_language
phonetic_transcription
word_class
syllabification
n_of_letters
n_of_phones
n_of_syllables
n_of_overlapping_letters
n_of_overlapping_phones
sw1_graphic
sw2_graphic
sw3_graphic
sw4_graphic
sw1_headmod
sw2_headmod
sw3_headmod
sw4_headmod
sw1_subdom
sw2_subdom
sw3_subdom
sw4_subdom
wf_process
lexsh_main
lexsh_sm
lexsh_whatm
split_point_1
split_point_2
split_point_3
"""

        respondent_id = r[1]
        nat_lang = r[2]

        # (nu_graphic, first_language, survey_language, image_id)
        d = OrderedDict()
        d['nu_graphic'] = r[12]
        d['first_language'], d['survey_language'] = res2lang[respondent_id]
        d['image_id'] = r[5]

        d['nu_phonetic'] = r[13]
        d['nu_word_class'] = r[14]
        d['nu_syllabic'] = r[15]
        d['nu_graphic_len'] = r[16]
        d['nu_phonetic_len'] = r[17]
        d['nu_syllabic_len'] = r[18]
        d['n_of_overlapping_letters'] = r[19]
        d['n_of_overlapping_phones'] = r[20]
        d['sw1_graphic'] = r[24]
        d['sw2_graphic'] = r[25]
        d['sw3_graphic'] = r[26]
        d['wf_process'] = r[11]
        d['lexsh_main'] = r[21]
        d['lexsh_sm'] = r[22]
        d['lexsh_whatm'] = r[23]
        d['split_point_1'] = r[101]
        d['split_point_2'] = r[102]

        table.add(d)
        data.append(list(d.values()))

        # # kontrola nativneho jazyka
        # if key[1] != nat_lang:
        #     print('LANG', res2lang[respondent_id][0], nat_lang, sep='\t|', file=stderr)
        #
        # # kontrola rovnakych informacii o rovnakych naming_unit
        # if key not in data:
        #     data[key] = d
        # else:
        #     s = data[key]
        #     for k in d.keys():
        #         if not d[k] and s[k]:
        #             d[k] = s[k]
        #         elif not s[k] and d[k]:
        #             s[k] = d[k]
        #     if d != data[key]:
        #         conflicts.add((int(key[3]), key[0]))  # image_id, naming_unit

    # list_of_data = list(map(lambda pair: [*pair[0], *pair[1].values()], data.items()))
    # if overlap:
    #     c.executemany(
    #         'INSERT IGNORE INTO naming_unit (naming_unit, first_language, survey_language, image_id, phonetic_transcription, '
    #         'word_class, syllabification, n_of_letters, n_of_phones, n_of_syllables, n_of_overlapping_letters, '
    #         'n_of_overlapping_phones, sw1_graphic, sw2_graphic, sw3_graphic, wf_process, lexsh_main, lexsh_sm, lexsh_whatm,'
    #         ' split_point_1, split_point_2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
    #         list_of_data
    #     )
    # else:
    #     c.executemany(
    #         'INSERT IGNORE INTO naming_unit (naming_unit, first_language, survey_language, image_id, phonetic_transcription, '
    #         'word_class, syllabification, n_of_letters, n_of_phones, n_of_syllables, '
    #         'sw1_graphic, sw2_graphic, sw3_graphic, wf_process, lexsh_main, lexsh_sm, lexsh_whatm,'
    #         ' split_point_1, split_point_2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
    #         list_of_data
    #     )
    # conn.commit()
    params = ', '.join([*kfields, *vfields])
    c.executemany(
        'INSERT IGNORE INTO naming_unit ('+params+') '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        data
    )

    table.write(filename)

    # with open('data/export/'+filename, 'w') as csvfile:
    #     writer = csv.writer(csvfile, delimiter='\t')
    #     writer.writerow(['image_id', 'naming_unit'])
    #     for row in sorted(conflicts, key=itemgetter(0)):
    #         writer.writerow(row)
    #
    # return len(conflicts) == 0


def import_source_words(conn, rows, filename):

    c = conn.cursor()
    res2lang = get_res2lang(c)

    # conflicts = set()

    # data = OrderedDict()
    data = []
    kfields = ('sw_graphic', 'first_language', 'survey_language', 'source_language')
    vfields = ('sw_phonetic', 'sw_word_class', 'sw_syllabic', 'sw_graphic_len', 'sw_phonetic_len',
               'sw_syllabic_len', 'frequency_in_snc')
    table = Table(kfields, vfields)

    for r in rows:

        respondent_id = r[1]
        keylangs = res2lang[respondent_id]

        for i in range(3):

            # stvorica (source_word, first_language, survey_language, source_language)
            key = (r[24+i], *keylangs, r[30+i])
            d = dict(zip(kfields, key))

            # d = OrderedDict()

            d['sw_phonetic'] = r[27+i]
            d['sw_word_class'] = r[33+i]
            d['sw_syllabic'] = r[36+i]
            d['sw_graphic_len'] = r[40+i]
            d['sw_phonetic_len'] = r[44+i]
            d['sw_syllabic_len'] = r[47+i]
            d['frequency_in_snc'] = r[50+i]

            table.add(d)
            data.append(list(d.values()))

            # if key not in data:
            #     data[key] = d
            # else:
            #     s = data[key]
            #     for k in d.keys():
            #         if not d[k] and s[k]:
            #             d[k] = s[k]
            #         elif not s[k] and d[k]:
            #             s[k] = d[k]
            #     if d != data[key]:
            #         conflicts.add(key[0])

    # list_of_data = [[*k, *v.values()] for k, v in data.items()]
    params = ', '.join([*kfields, *vfields])
    c.executemany(
        'INSERT IGNORE INTO source_word ('+params+') VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        data
    )
    # conn.commit()

    table.write(filename)

    # with open('data/export/'+filename, 'w') as fp:
    #
    #     for source_word in conflicts:
    #         print(source_word, file=fp)
    #
    # return len(conflicts) == 0


def import_splinters(conn, rows, filename):
    c = conn.cursor()
    res2lang = get_res2lang(c)
    # conflicts = set()
    # data = OrderedDict()

    data = []
    kfields = ('nu_graphic', 'first_language', 'survey_language', 'image_id', 'type_of_splinter')
    vfields = ('sw1_splinter', 'sw2_splinter', 'sw3_splinter', 'sw1_splinter_len',
               'sw2_splinter_len', 'sw3_splinter_len')
    table = Table(kfields, vfields)

    types = (
        'graphic strict',
        'graphic modified',
        'phonetic strict',
        'phonetic modified'
    )

    for r in rows:
        respondent_id = r[1]

        langs = res2lang[respondent_id]
        # (nu_graphic, first_language, survey_language, image_id)
        pre_d = {
            'nu_graphic': r[12],
            'first_language': langs[0],
            'survey_language': langs[1],
            'image_id': r[5]
        }

        for i, type_of_splinter in enumerate(types):
            d = dict(pre_d)
            d['type_of_splinter'] = type_of_splinter
            # key = (*prekey, type_of_splinter)
            # d = OrderedDict()
            d['sw1_splinter'] = r[53+3*i]
            d['sw2_splinter'] = r[54+3*i]
            d['sw3_splinter'] = r[55+3*i]
            d['sw1_splinter_len'] = r[65+3*i]
            d['sw2_splinter_len'] = r[66+3*i]
            d['sw3_splinter_len'] = r[67+3*i]

            table.add(d)
            data.append(list(d.values()))

            # if key not in data:
            #     data[key] = d
            # else:
            #     s = data[key]
            #     for k in d.keys():
            #         if not d[k] and s[k]:
            #             d[k] = s[k]
            #         elif not s[k] and d[k]:
            #             s[k] = d[k]
            #     if d != data[key]:
            #         conflicts.add((key[0], type_of_splinter))

    # list_of_data = [[*k, *v.values()] for k, v in data.items()]
    params = ', '.join([*kfields, *vfields])
    c.executemany(
        'INSERT IGNORE INTO splinter ('+params+') '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        # list_of_data
        data
    )
    # conn.commit()

    table.write(filename)

    # with open('data/export/'+filename, 'w') as fp:
    #     wr = csv.writer(fp, delimiter='\t')
    #     wr.writerow(('naming_unit', 'type_of_splinter'))
    #     for row in sorted(conflicts, key=itemgetter(0)):
    #         wr.writerow(row)
    #
    # return len(conflicts) == 0


def created_name_units():
    """0, END, Number of Order
1, None, ID
2, Nat lang, None
3, None, Age
4, None, Sex
5, None, Object
6, None, Object info
7, None, OT
8, None, W-F Type
9, None, Morphological Type
10, None, WF Rule
11, None, Main W-f Process
12, None, Naming Unit
13, Phonetic transcription, None
14, None, Word class
15, None, Syllabification
16, N of letters, None
17, N of phones, None
18, N of syllabes, None
19, Number of OVERLAPPING LETTERS, None
20, N of OVERLAPPING phones, None
21, Type of Lexical SHORTENING, MAIN
22, None, S/M
23, None, What M
24, Graphic form of source words, SW1
25, None, SW2
26, None, SW3
27, Phonetic transcription of source words, SW1
28, None, SW2
29, None, SW3
30, Source language, SW1
31, None, SW2
32, None, SW3
33, Word class, SW1
34, None, SW2
35, None, SW3
36, Syllabification, SW 1
37, None, SW 2
38, None, SW 3
39, None, SW4
40, Number of letters, SW1
41, None, SW2
42, None, SW3
43, None, SW4
44, Number of phonemes, SW 1
45, None, SW 2
46, None, SW 3
47, Number of syllables, SW 1
48, None, SW 2
49, None, SW 3
50, Frequency in SNC, SW 1
51, None, SW 2
52, None, SW 3
53, SPLINTER (graphic form), SW 1
54, None, SW 2
55, None, SW 3
56, SPLINTER (graphic form ignoring diacritics, i/y, SW 1
57, None, SW 2
58, None, SW 3
59, SPLINTER (phonetic transcription), None
60, None, None
61, None, None
62, SPLINTER (transcription ignoring acutes), SW 1
63, None, SW 2
64, None, SW 3
65, Graphic SPLINTER length in letters, SW 1
66, None, SW 2
67, None, SW 3
68, Graphic SPLINTER without diacritics length, SW 1
69, None, SW 2
70, None, SW 3
71, Phonetic SPLINTER length in phones, SW 1
72, None, SW 2
73, None, SW 3
74, Phonetic SPLINTER without acutes length, SW 1
75, None, SW 2
76, None, SW 3
77, Graphic SPLINTER length / SW length in letters, SW 1
78, None, SW 2
79, None, SW 3
80, Graphic SPLINTER without diacritics length / SW length in letters, SW 1
81, None, SW 2
82, None, SW 3
83, Phonetic SPLINTER length / SW length in phones, SW 1
84, None, SW 2
85, None, SW 3
86, Phonetic SPLINTER without acutes length / SW length in phones, SW 1
87, None, SW 2
88, None, SW 3
89, Graphic SPLINTER length / NU length in letters, SW 1
90, None, SW 2
91, None, SW 3
92, Graphic SPLINTER without diacritics length / NU length in letters, SW 1
93, None, SW 2
94, None, SW 3
95, Phonetic SPLINTER length / NU length in phones, SW 1
96, None, SW 2
97, None, SW 3
98, Phonetic SPLINTER without acutes length / NU length in phones, SW 1
99, None, SW 2
100, None, SW 3
101, SPLIT POINT Placement, SW 1
102, None, SW 2
103, None, SW 3"""

    with open('data/sk_overview_created_name_units.csv') as csvfile:

        rows = tsv_reader(csvfile)
        next(rows)
        next(rows)

        # vytvori subor export/sk_different_naming_units.tsv
        # iba cita z response

        #

        # vytvori subor podla zadania, ak su konflikty
        # cita z respondent
        # zapisuje do naming_unit

        # lines = list(rows)
        # ok = import_naming_units(conn, lines, True, 'sk_generalization_naming_units.tsv')
        # print(ok)
        ## ok = import_naming_units(conn, lines, False, 'sk_generalization_naming_units_without_overlap.tsv')
        ## print(ok)

        # cita z respondent
        # zapisuje do source_words
        # do suboru zapise, pri ktorych source_words su konflikty
        # v pripade konfliktu je v DB prvy vyskyt

        # ok = import_source_words(conn, rows, 'sk_generalization_source_words.txt')
        # print(ok)

        ok = import_splinters(conn, list(rows), 'sk_generalization_splinters')
        print(ok)


with open('data/sk_overview_created_name_units.csv') as csvfile:
    rows = list(tsv_reader(csvfile))
    rows.pop(0)
    rows.pop(0)
    with Connection() as conn:
        # check_responses(conn, rows, 'sk_different_naming_units.tsv')
        # import_naming_units(conn, rows, 'sk_generalization_naming_units.tsv')
        # import_source_words(conn, rows, 'sk_generalization_source_words.tsv')
        import_splinters(conn, rows, 'sk_generalization_splinters.tsv')
