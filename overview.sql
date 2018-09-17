CREATE VIEW `overview` AS
  select
    `RS`.`respondent_id` AS `respondent_id`,
    `RT`.`age` AS `age`,
    `RT`.`sex` AS `sex`,
    N.*
  from
    (
        (`response` `RS` left join `respondent` `RT` on((`RS`.`respondent_id` = `RT`.`respondent_id`)))
        left join `nu_full` `N` on(((`N`.`nu_graphic` = `RS`.`nu_graphic`) and (`N`.`image_id` = `RS`.`image_id`) and (`N`.`first_language` = `RT`.`first_language`) and (`N`.`survey_language` = `RT`.`survey_language`)))
    )
