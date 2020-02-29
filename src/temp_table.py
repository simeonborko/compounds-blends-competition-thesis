def create_response_combined(conn):

    conn.cursor().execute("""CREATE OR REPLACE TEMPORARY TABLE response_combined (
  respondent_id varchar(10) not null,
  image_id int(11) not null,
  nu_original varchar(500) not null,
  nu_modified varchar(500) null,
  nu_graphic varchar(500) not null,
  INDEX (respondent_id, image_id)
);""")
    conn.cursor().execute("""INSERT INTO response_combined
  (SELECT O.respondent_id, O.image_id, O.nu_original, M.nu_modified,
  IF(M.nu_modified is null, O.nu_original, M.nu_modified) as nu_graphic
   FROM response_original O
LEFT JOIN response_modified M ON
    M.respondent_id = O.respondent_id AND M.image_id = O.image_id);""")


def create_respondent_response(conn):
    conn.cursor().execute("""CREATE OR REPLACE TEMPORARY TABLE respondent_response (
  respondent_id varchar(10) not null,
  first_language char(2) not null,
  survey_language char(2) not null,
  age int(11),
  sex char(1),
  image_id int(11) not null,
  nu_original varchar(500) not null,
  nu_modified varchar(500),
  nu_graphic varchar(500) not null,
  INDEX (nu_graphic, image_id, first_language, survey_language)
);""")
    conn.cursor().execute("""INSERT INTO respondent_response (
  SELECT RT.respondent_id,
    RT.first_language,
    RT.survey_language,
    RT.age,
    RT.sex,
    RS.image_id,
    RS.nu_original,
    RS.nu_modified,
    RS.nu_graphic
  FROM response_combined RS
  LEFT JOIN respondent RT
    ON RS.respondent_id = RT.respondent_id
);""")
