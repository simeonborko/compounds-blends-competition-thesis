CREATE OR REPLACE VIEW overview AS
SELECT
  RS.respondent_id as respondent_id,
  RT.age as age,
  RT.sex as sex,
  N.*
FROM
    (
      (response_combined RS
      LEFT JOIN `respondent` RT ON
        RS.respondent_id = RT.respondent_id)
      LEFT JOIN `nu_full` N ON
        N.nu_graphic = RS.nu_modified
        AND N.image_id = RS.image_id
        AND N.first_language = RT.first_language
        AND N.survey_language = RT.survey_language
    );