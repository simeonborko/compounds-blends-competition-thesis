"""
0 | None | Number of Order
1 | None | ID
2 | None | Nat lang
3 | None | Age
4 | None | Sex
5 | None | Object
6 | None | Object Info
7 | None | OT
8 | None | W-F Type
9 | None | Morphological Type
10 | None | WF Rule
11 | None | Main W-f Process
12 | None | Naming Unit
13 | None | Phonetic transcription
14 | None | WC
15 | None | Syllabification
16 | None | N of letters
17 | None | N of phones
18 | None | N of syllables
19 | None | N of overlapping letters
20 | Type of lexical shortening | MAIN
21 | None | S/M
22 | None | what M
23 | Graphic form of source words | SW1
24 | None | SW2
25 | None | SW3
26 | None | SW4
27 | Phonetic transcription of source words | SW1
28 | None | SW2
29 | None | SW3
30 | None | SW4
31 | Source language of source words | SW1
32 | None | SW2
33 | None | SW3
34 | None | SW4
35 | Word class of source words | SW1
36 | None | SW2
37 | None | SW3
38 | None | SW4
39 | Syllabification | SW1
40 | None | SW2
41 | None | SW3
42 | None | SW4
43 | Number of letters | SW1
44 | None | SW2
45 | None | SW3
46 | None | SW4
47 | Number of phones | SW1
48 | None | SW2
49 | None | SW3
50 | None | SW4
51 | Number of syllables | SW1
52 | None | SW2
53 | None | SW3
54 | None | SW4
55 | Frequency in corpus (which?) | SW1
56 | None | SW2
57 | None | SW3
58 | None | SW4
59 | Graphic form of splinter | SW1
60 | None | SW2
61 | None | SW3
62 | None | SW4
63 | Graphic SPLINTER length in letters | SW1
64 | None | SW2
65 | None | SW3
66 | None | SW4
67 | Phonetic SPLINTER length in phones | None
68 | None | None
69 | None | None
70 | None | None
"""
import csv
from collections import OrderedDict
from operator import itemgetter

from tools.tools import Connection, tsv_reader, get_res2lang, get_lang2code, Table
from sys import stderr


def update_respondent(conn, rows):
    c = conn.cursor()
    lang2code = get_lang2code(c)
    data = OrderedDict()
    for r in rows:
        # respondent_id
        key = r[1]
        # first_language, age, sex
        d = (lang2code[r[2]], r[3], r[4])

        if key not in data:
            data[key] = d
        elif d != data[key]:
            print('RESPONDENT', r[0], file=stderr)

    c.executemany(
        'UPDATE respondent SET first_language_tmp=%s, age_tmp=%s, sex_tmp=%s '
        'WHERE respondent_id=%s',
        [[*v, k] for k, v in data.items()]
    )
    conn.commit()


def check_responses(conn, rows, filename):
    # kontrola ci lydka neupravila Naming unit
    n_of_conflicts = 0
    divided = {}
    with open('data/export/'+filename, 'w') as outf:
        wr = csv.writer(outf, delimiter='\t')
        wr.writerow(('id', 'respondent_id', 'image_id', 'naming_unit', 'DB naming_unit'))
        c = conn.cursor()
        for r in rows:
            response_id = r[0]
            respondent_id = r[1]
            image_id = r[5]
            naming_unit = r[12]

            key = (respondent_id, image_id)
            divided.setdefault(key, 0)
            divided[key] += 1

            # je nieco take aj v databaze?
            c.execute(
                'SELECT COUNT(*) FROM response WHERE respondent_id = %s AND image_id = %s AND naming_unit = %s',
                (respondent_id, image_id, naming_unit)
            )

            # ak ano, pokracuj
            if c.fetchone()[0] == 1:
                continue

            # ak nie, zisti, co mame v db

            # c.execute(
            #     'UPDATE response SET naming_unit_tmp = %s WHERE respondent_id = %s AND image_id = %s',
            #     (naming_unit, respondent_id, image_id)
            # )
            c.execute(
                'SELECT naming_unit FROM response WHERE respondent_id = %s AND image_id = %s LIMIT 1',
                (respondent_id, image_id)
            )

            d_naming_unit = next(c)[0]

            if naming_unit != d_naming_unit:
                wr.writerow((
                    response_id,
                    respondent_id,
                    image_id,
                    naming_unit,
                    d_naming_unit
                ))
                n_of_conflicts += 1

    # conn.commit()

    # for k, v in divided.items():
    #     if v > 1:
    #         print(*k, sep='\t', file=stderr)
    print('Check responses conflicts:', n_of_conflicts)


def import_naming_units(conn, rows, filename):
    c = conn.cursor()
    res2lang = get_res2lang(c)
    # conflicts = set()
    data = []
    table = Table(
        ('nu_graphic', 'first_language', 'survey_language', 'image_id'),
        ('nu_phonetic', 'nu_word_class', 'nu_syllabic', 'nu_graphic_len', 'nu_phonetic_len', 'nu_syllabic_len',
         'n_of_overlapping_letters', 'lexsh_main', 'lexsh_sm', 'lexsh_whatm', 'sw1_graphic', 'sw2_graphic',
         'sw3_graphic', 'sw4_graphic', 'wf_process')
    )
    for r in rows:
        respondent_id = r[1]

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
        d['lexsh_main'] = r[20]
        d['lexsh_sm'] = r[21]
        d['lexsh_whatm'] = r[22]
        d['sw1_graphic'] = r[23]
        d['sw2_graphic'] = r[24]
        d['sw3_graphic'] = r[25]
        d['sw4_graphic'] = r[26]
        d['wf_process'] = r[11]

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
        #         conflicts.add((int(key[3]), key[0]))  # image_id, naming_unit

    c.executemany(
        'INSERT IGNORE INTO naming_unit (nu_graphic, first_language, survey_language, image_id, nu_phonetic, '
        'nu_word_class, nu_syllabic, nu_graphic_len, nu_phonetic_len, nu_syllabic_len, n_of_overlapping_letters, '
        'lexsh_main, lexsh_sm, lexsh_whatm, sw1_graphic, sw2_graphic, sw3_graphic, sw4_graphic, wf_process) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        #[[*k, *v.values()] for k, v in data.items()]
        data
    )
    # conn.commit()

    table.write(filename)

    # with open('data/export/'+filename, 'w') as fp:
    #     writer = csv.writer(fp, delimiter='\t')
    #     writer.writerow(('image_id', 'naming_unit'))
    #     for row in sorted(conflicts, key=itemgetter(0)):
    #         writer.writerow(row)
    #
    # print('Naming units conflicts:', len(conflicts))


def import_source_words(conn, rows, filename):
    c = conn.cursor()
    res2lang = get_res2lang(c)

    # conflicts = set()

    # data = OrderedDict()
    data = []
    table = Table(
        ('sw_graphic', 'first_language', 'survey_language', 'source_language'),
        ('sw_phonetic', 'sw_word_class', 'sw_syllabic', 'sw_graphic_len', 'sw_phonetic_len', 'sw_syllabic_len')
    )

    for r in rows:
        respondent_id = r[1]
        keylangs = res2lang[respondent_id]

        for i in range(4):
            d = {
                'sw_graphic': r[23+i],
                'first_language': keylangs[0],
                'survey_language': keylangs[1],
                'source_language': r[31+i]
            }
            # stvorica (source_word, first_language, survey_language, source_language)
            # key = (r[23+i], *keylangs, r[31+i])

            # d = OrderedDict()

            d['sw_phonetic'] = r[27+i]
            d['sw_word_class'] = r[35+i]
            d['sw_syllabic'] = r[39+i]
            d['sw_graphic_len'] = r[43+i]
            d['sw_phonetic_len'] = r[47+i]
            d['sw_syllabic_len'] = r[51+i]

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

    c.executemany(
        'INSERT IGNORE INTO source_word (sw_graphic, first_language, survey_language, source_language, '
        'sw_phonetic, sw_word_class, sw_syllabic, sw_graphic_len, sw_phonetic_len, sw_syllabic_len) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        # [[*k, *v.values()] for k, v in data.items()]
        data
    )
    # conn.commit()

    table.write(filename)

    # with open('data/export/'+filename, 'w') as fp:
    #     for sw in conflicts:
    #         print(sw, file=fp)
    #
    # print('Source words conflicts:', len(conflicts))


def import_splinters(conn, rows, filename):
    """Berie iba graficky splinter a berie ho ako strict."""
    c = conn.cursor()
    res2lang = get_res2lang(c)
    # conflicts = set()
    # data = OrderedDict()
    data = []
    kfields = ('nu_graphic', 'first_language', 'survey_language', 'image_id', 'type_of_splinter')
    vfields = ('sw1_splinter', 'sw2_splinter', 'sw3_splinter', 'sw4_splinter', 'sw1_splinter_len',
         'sw2_splinter_len', 'sw3_splinter_len', 'sw4_splinter_len')
    table = Table(kfields, vfields)

    for r in rows:
        respondent_id = r[1]

        # (nu_graphic, first_language, survey_language, image_id, type_of_splinter)
        key = (r[12], *res2lang[respondent_id], r[5], 'graphic strict')
        d = dict(zip(kfields, key))
        d.update(dict(zip(vfields, r[59:67])))

        table.add(d)
        data.append(list(d.values()))

        # if key not in data:
        #     data[key] = d
        # else:
        #     s = data[key]
        #     for k in range(len(d)):
        #         if not d[k] and s[k]:
        #             d[k] = s[k]
        #         elif not s[k] and d[k]:
        #             s[k] = d[k]
        #     if d != data[key]:
        #         conflicts.add(key[0])  # nu_graphic

    c.executemany(
        'INSERT IGNORE INTO splinter (nu_graphic, first_language, survey_language, image_id, type_of_splinter, '
        'sw1_splinter, sw2_splinter, sw3_splinter, sw4_splinter, '
        'sw1_splinter_len, sw2_splinter_len, sw3_splinter_len, sw4_splinter_len) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        # [[*k, *v] for k, v in data.items()]
        data
    )
    # conn.commit()

    table.write(filename)

    # with open('data/export/'+filename, 'w') as fp:
    #     for x in conflicts:
    #         print(x, file=fp)
    #
    # print('Splinters conflicts:', len(conflicts))


with open('data/en_overview.csv') as csvfile:
    rows = list(tsv_reader(csvfile))
    rows.pop(0)
    rows.pop(0)
    with Connection() as conn:
        # update_respondent(conn, rows)
        check_responses(conn, rows, 'en_different_naming_units.tsv')
        import_naming_units(conn, rows, 'en_generalization_naming_units.tsv')
        import_source_words(conn, rows, 'en_generalization_source_words.tsv')
        import_splinters(conn, rows, 'en_generalization_splinters.tsv')
