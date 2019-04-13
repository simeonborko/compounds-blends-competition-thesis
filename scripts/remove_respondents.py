"""
Odstrani respondentov a ich odpovede.
Podmienky: first_language not in [SK, EN] or age < 16
"""

from tools import Connection

if __name__ == '__main__':
    with Connection() as conn:

        c = conn.cursor()
        c.execute(
            "SELECT respondent_id FROM respondent WHERE first_language != 'SK' AND first_language != 'EN' OR age < 16 OR sex != 'F' AND sex != 'M'"
        )
        res_ids = [res_id for res_id, in c]
        for res_id in res_ids:

            conn.cursor().execute(
                "DELETE FROM response_original WHERE respondent_id = %s",
                (res_id, )
            )
            conn.cursor().execute(
                "DELETE FROM response_modified WHERE respondent_id = %s",
                (res_id, )
            )
            conn.cursor().execute(
                "DELETE FROM respondent WHERE respondent_id = %s",
                (res_id, )
            )

        conn.commit()
