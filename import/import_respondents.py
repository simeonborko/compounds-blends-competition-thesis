import csv
from datetime import datetime
from collections import OrderedDict
from tools import Connection

en_file = 'data/en_responses.csv'
sk_file = 'data/sk_responses.csv'

# respondent_id	int(11)
# first_language	varchar(500)
# second_language	varchar(500)
# other_language	varchar(500)
# age	int(11)
# sex	varchar(500)
# employment	varchar(500)
# education	varchar(500)
# birth_place	varchar(500)
# year_of_birth	int(11)
# responding_date	date


def respondent_info():

    data = []

    for file, lang in ((en_file, 'EN'), (sk_file, 'SK')):
        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            next(reader)
            for l in reader:
                d = OrderedDict()
                d['respondent_id'] = int(l[0])
                d['first_lang'] = l[50]
                d['second_lang'] = l[51]
                d['other_lang'] = l[52]
                d['age'] = l[45]
                d['sex'] = l[46]
                d['employment'] = l[47]
                d['education'] = l[49]
                d['birth_place'] = l[48]
                d['year_of_birth'] = l[9]
                d['responding_date'] = datetime.strptime(l[2], '%m/%d/%Y %I:%M:%S %p').date()
                d['survey_lang'] = lang
                data.append(list(d.values()))
                #print("""INSERT INTO respondent VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(*list(d.values())))
                # cursor.execute('INSERT INTO respondent VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', list(d.values()))

    # with open('tmp', 'w') as csvfile:
    #     writer = csv.writer(csvfile, delimiter='\t')
    #     for line in data:
    #         writer.writerow(line)

    return data


with Connection() as conn:
    data = respondent_info()
    conn.cursor().executemany(
        'INSERT IGNORE INTO respondent (respondent_id, first_language_original, second_language, other_language, age, '
        'sex_original, employment, education, birth_place, year_of_birth, responding_date, survey_language) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', data)
    conn.commit()
