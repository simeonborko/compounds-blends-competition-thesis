CREATE OR REPLACE VIEW respondent_response AS
  (SELECT
     RT.*,
     RS.image_id,
     RS.nu_original,
     RS.nu_modified
   FROM response_combined RS LEFT JOIN respondent RT ON RS.respondent_id = RT.respondent_id
  );