import csv
from tools import Connection

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
                respondent_id = l[0].strip()
                for image_id, naming_unit in enumerate(l[10:45], 1):
                    data.append([respondent_id, image_id, naming_unit.strip()])
    return data


with Connection() as conn:

    conn.cursor().execute("DELETE FROM response_original")

    data = response_info()
    conn.cursor().executemany(
        'INSERT INTO response_original (respondent_id, image_id, nu_original) VALUES (%s,%s,%s)',
        data
    )
    conn.commit()
