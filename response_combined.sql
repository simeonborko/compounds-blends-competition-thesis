CREATE OR REPLACE VIEW `response_combined` AS
SELECT O.respondent_id, O.image_id, O.nu_original, M.nu_modified FROM response_original O
LEFT JOIN response_modified M ON
    M.respondent_id = O.respondent_id AND M.image_id = O.image_id;