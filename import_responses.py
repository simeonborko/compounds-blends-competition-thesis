import csv
from connection import Connection

en_file = 'data/en_responses.csv'
sk_file = 'data/sk_responses.csv'


def response_info():
    data = []
    for file in (en_file, sk_file):
        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            next(reader)
            for l in reader:
                respondent_id = l[0]
                for image_id, naming_unit in enumerate(l[10:45], 1):
                    data.append([respondent_id, image_id, naming_unit])
    return data


with Connection() as conn:
    data = response_info()
    conn.cursor().executemany(
        'INSERT INTO response (respondent_id, image_id, naming_unit) VALUES (%s,%s,%s)',
        data
    )
    conn.commit()
