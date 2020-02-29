import csv

from src.tools import Connection

with Connection() as conn:
    c = conn.cursor()
    c.execute("SELECT respondent_id, image_id, nu_original FROM response_original")
    originals = {r[:2]: r[2] for r in c}

    data = []

    overviews = (
        'data/sk_overview_created_name_units.csv',
        'data/en_overview.csv'
    )

    for ov in overviews:

        with open(ov) as fp:
            reader = csv.reader(fp, delimiter='\t')
            next(reader)
            next(reader)
            for row in reader:
                key = row[1].strip(), int(row[5])
                nu = row[12].strip()
                if originals[key] != nu and nu:
                    data.append((*key, nu))

    c = conn.cursor()
    c.execute("DELETE FROM response_modified")
    res = c.executemany(
        "INSERT INTO response_modified (respondent_id, image_id, nu_modified) VALUES (%s, %s, %s)",
        data
    )
    print(res)
    res = c.execute(
        "UPDATE response_modified SET nu_modified = %s WHERE nu_modified = %s",
        ('Indian Butterfly', 'Indian Butterbutterfly')
    )
    print(res)
    conn.commit()

