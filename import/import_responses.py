import csv
from src.tools import Connection

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
                    data.append([respondent_id, image_id, naming_unit.replace(b"\xF0\x9F\x98\x89".decode('utf-8'), '').strip()])
    return data


with Connection() as conn:

    conn.cursor().execute("DELETE FROM response_original")

    data = response_info()
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO response_original (respondent_id, image_id, nu_original) VALUES (%s,%s,%s)',
        data
    )
    # print(cursor._last_executed.decode('utf-8'))
    conn.commit()
