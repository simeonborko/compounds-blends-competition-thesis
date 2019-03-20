"""
Pridat what_connect_element a dom_half do nu_full.
"""

from yoyo import step

NEW_VIEW = """
CREATE OR REPLACE VIEW `nu_full` AS
  select
    `NU`.`nu_graphic` AS `nu_graphic`,
    `NU`.`first_language` AS `first_language`,
    `NU`.`survey_language` AS `survey_language`,
    NU.wf_process as wf_process,
    NU.wfp_specification as wfp_specification,
    NU.wfp_strict_modification as wfp_strict_modification,
    NU.connect_element as connect_element,
    NU.what_connect_element as what_connect_element,
    NU.dom_half as dom_half,
    `NU`.`image_id` AS `image_id`,
    `NU`.`nu_phonetic` AS `nu_phonetic`,
    `NU`.`nu_syllabic` AS `nu_syllabic`,
    `NU`.`nu_graphic_len` AS `nu_graphic_len`,
    `NU`.`nu_phonetic_len` AS `nu_phonetic_len`,
    `NU`.`nu_syllabic_len` AS `nu_syllabic_len`,
    `NU`.`sw1_graphic` AS `sw1_graphic`,
    `NU`.`sw2_graphic` AS `sw2_graphic`,
    `NU`.`sw3_graphic` AS `sw3_graphic`,
    `NU`.`sw4_graphic` AS `sw4_graphic`,
    `SW1`.`sw_word_class` AS `sw1_word_class`,
    `SW2`.`sw_word_class` AS `sw2_word_class`,
    `SW3`.`sw_word_class` AS `sw3_word_class`,
    `SW4`.`sw_word_class` AS `sw4_word_class`,
    `SW1`.`source_language` AS `sw1_source_language`,
    `SW2`.`source_language` AS `sw2_source_language`,
    `SW3`.`source_language` AS `sw3_source_language`,
    `SW4`.`source_language` AS `sw4_source_language`,
    SW1.proper_name AS sw1_proper_name,
    SW2.proper_name AS sw2_proper_name,
    SW3.proper_name AS sw3_proper_name,
    SW4.proper_name AS sw4_proper_name,
    `SW1`.`sw_graphic_len` AS `sw1_graphic_len`,
    `SW2`.`sw_graphic_len` AS `sw2_graphic_len`,
    `SW3`.`sw_graphic_len` AS `sw3_graphic_len`,
    `SW4`.`sw_graphic_len` AS `sw4_graphic_len`,
    `SW1`.`sw_phonetic` AS `sw1_phonetic`,
    `SW2`.`sw_phonetic` AS `sw2_phonetic`,
    `SW3`.`sw_phonetic` AS `sw3_phonetic`,
    `SW4`.`sw_phonetic` AS `sw4_phonetic`,
    `SW1`.`sw_phonetic_len` AS `sw1_phonetic_len`,
    `SW2`.`sw_phonetic_len` AS `sw2_phonetic_len`,
    `SW3`.`sw_phonetic_len` AS `sw3_phonetic_len`,
    `SW4`.`sw_phonetic_len` AS `sw4_phonetic_len`,
    `SW1`.`sw_syllabic` AS `sw1_syllabic`,
    `SW2`.`sw_syllabic` AS `sw2_syllabic`,
    `SW3`.`sw_syllabic` AS `sw3_syllabic`,
    `SW4`.`sw_syllabic` AS `sw4_syllabic`,
    `SW1`.`sw_syllabic_len` AS `sw1_syllabic_len`,
    `SW2`.`sw_syllabic_len` AS `sw2_syllabic_len`,
    `SW3`.`sw_syllabic_len` AS `sw3_syllabic_len`,
    `SW4`.`sw_syllabic_len` AS `sw4_syllabic_len`,
    `SW1`.`frequency_in_snc` AS `sw1_frequency_in_snc`,
    `SW2`.`frequency_in_snc` AS `sw2_frequency_in_snc`,
    `SW3`.`frequency_in_snc` AS `sw3_frequency_in_snc`,
    `SW4`.`frequency_in_snc` AS `sw4_frequency_in_snc`,
    `GS`.`type_of_splinter` AS `gs_name`,
    `GS`.`sw1_splinter` AS `gs_sw1_splinter`,
    `GS`.`sw2_splinter` AS `gs_sw2_splinter`,
    `GS`.`sw3_splinter` AS `gs_sw3_splinter`,
    `GS`.`sw4_splinter` AS `gs_sw4_splinter`,
    `GS`.`sw1_splinter_len` AS `gs_sw1_splinter_len`,
    `GS`.`sw2_splinter_len` AS `gs_sw2_splinter_len`,
    `GS`.`sw3_splinter_len` AS `gs_sw3_splinter_len`,
    `GS`.`sw4_splinter_len` AS `gs_sw4_splinter_len`,
    (`GS`.`sw1_splinter_len` / `SW1`.`sw_graphic_len`) AS `gs_sw1_splinter_len_to_sw_len`,
    (`GS`.`sw2_splinter_len` / `SW2`.`sw_graphic_len`) AS `gs_sw2_splinter_len_to_sw_len`,
    (`GS`.`sw3_splinter_len` / `SW3`.`sw_graphic_len`) AS `gs_sw3_splinter_len_to_sw_len`,
    (`GS`.`sw4_splinter_len` / `SW4`.`sw_graphic_len`) AS `gs_sw4_splinter_len_to_sw_len`,
    (`GS`.`sw1_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw1_splinter_len_to_nu_len`,
    (`GS`.`sw2_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw2_splinter_len_to_nu_len`,
    (`GS`.`sw3_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw3_splinter_len_to_nu_len`,
    (`GS`.`sw4_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw4_splinter_len_to_nu_len`,
    `GM`.`type_of_splinter` AS `gm_name`,
    `GM`.`sw1_splinter` AS `gm_sw1_splinter`,
    `GM`.`sw2_splinter` AS `gm_sw2_splinter`,
    `GM`.`sw3_splinter` AS `gm_sw3_splinter`,
    `GM`.`sw4_splinter` AS `gm_sw4_splinter`,
    `GM`.`sw1_splinter_len` AS `gm_sw1_splinter_len`,
    `GM`.`sw2_splinter_len` AS `gm_sw2_splinter_len`,
    `GM`.`sw3_splinter_len` AS `gm_sw3_splinter_len`,
    `GM`.`sw4_splinter_len` AS `gm_sw4_splinter_len`,
    (`GM`.`sw1_splinter_len` / `SW1`.`sw_graphic_len`) AS `gm_sw1_splinter_len_to_sw_len`,
    (`GM`.`sw2_splinter_len` / `SW2`.`sw_graphic_len`) AS `gm_sw2_splinter_len_to_sw_len`,
    (`GM`.`sw3_splinter_len` / `SW3`.`sw_graphic_len`) AS `gm_sw3_splinter_len_to_sw_len`,
    (`GM`.`sw4_splinter_len` / `SW4`.`sw_graphic_len`) AS `gm_sw4_splinter_len_to_sw_len`,
    (`GM`.`sw1_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw1_splinter_len_to_nu_len`,
    (`GM`.`sw2_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw2_splinter_len_to_nu_len`,
    (`GM`.`sw3_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw3_splinter_len_to_nu_len`,
    (`GM`.`sw4_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw4_splinter_len_to_nu_len`,
    `PS`.`type_of_splinter` AS `ps_name`,
    `PS`.`sw1_splinter` AS `ps_sw1_splinter`,
    `PS`.`sw2_splinter` AS `ps_sw2_splinter`,
    `PS`.`sw3_splinter` AS `ps_sw3_splinter`,
    `PS`.`sw4_splinter` AS `ps_sw4_splinter`,
    `PS`.`sw1_splinter_len` AS `ps_sw1_splinter_len`,
    `PS`.`sw2_splinter_len` AS `ps_sw2_splinter_len`,
    `PS`.`sw3_splinter_len` AS `ps_sw3_splinter_len`,
    `PS`.`sw4_splinter_len` AS `ps_sw4_splinter_len`,
    (`PS`.`sw1_splinter_len` / `SW1`.`sw_phonetic_len`) AS `ps_sw1_splinter_len_to_sw_len`,
    (`PS`.`sw2_splinter_len` / `SW2`.`sw_phonetic_len`) AS `ps_sw2_splinter_len_to_sw_len`,
    (`PS`.`sw3_splinter_len` / `SW3`.`sw_phonetic_len`) AS `ps_sw3_splinter_len_to_sw_len`,
    (`PS`.`sw4_splinter_len` / `SW4`.`sw_phonetic_len`) AS `ps_sw4_splinter_len_to_sw_len`,
    (`PS`.`sw1_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw1_splinter_len_to_nu_len`,
    (`PS`.`sw2_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw2_splinter_len_to_nu_len`,
    (`PS`.`sw3_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw3_splinter_len_to_nu_len`,
    (`PS`.`sw4_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw4_splinter_len_to_nu_len`,
    `PM`.`type_of_splinter` AS `pm_name`,
    `PM`.`sw1_splinter` AS `pm_sw1_splinter`,
    `PM`.`sw2_splinter` AS `pm_sw2_splinter`,
    `PM`.`sw3_splinter` AS `pm_sw3_splinter`,
    `PM`.`sw4_splinter` AS `pm_sw4_splinter`,
    `PM`.`sw1_splinter_len` AS `pm_sw1_splinter_len`,
    `PM`.`sw2_splinter_len` AS `pm_sw2_splinter_len`,
    `PM`.`sw3_splinter_len` AS `pm_sw3_splinter_len`,
    `PM`.`sw4_splinter_len` AS `pm_sw4_splinter_len`,
    (`PM`.`sw1_splinter_len` / `SW1`.`sw_phonetic_len`) AS `pm_sw1_splinter_len_to_sw_len`,
    (`PM`.`sw2_splinter_len` / `SW2`.`sw_phonetic_len`) AS `pm_sw2_splinter_len_to_sw_len`,
    (`PM`.`sw3_splinter_len` / `SW3`.`sw_phonetic_len`) AS `pm_sw3_splinter_len_to_sw_len`,
    (`PM`.`sw4_splinter_len` / `SW4`.`sw_phonetic_len`) AS `pm_sw4_splinter_len_to_sw_len`,
    (`PM`.`sw1_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw1_splinter_len_to_nu_len`,
    (`PM`.`sw2_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw2_splinter_len_to_nu_len`,
    (`PM`.`sw3_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw3_splinter_len_to_nu_len`,
    (`PM`.`sw4_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw4_splinter_len_to_nu_len`
  from (
      (
          (
              (
                  (
                      (
                          (
                              (
                                  (`naming_unit` `NU`)
                                  left join `source_word` `SW1` on(((`NU`.`first_language` = `SW1`.`first_language`) and (`NU`.`survey_language` = `SW1`.`survey_language`) and (`NU`.`sw1_graphic` = `SW1`.`sw_graphic`)))
                              )
                              left join `source_word` `SW2` on(((`NU`.`first_language` = `SW2`.`first_language`) and (`NU`.`survey_language` = `SW2`.`survey_language`) and (`NU`.`sw2_graphic` = `SW2`.`sw_graphic`)))
                          )
                          left join `source_word` `SW3` on(((`NU`.`first_language` = `SW3`.`first_language`) and (`NU`.`survey_language` = `SW3`.`survey_language`) and (`NU`.`sw3_graphic` = `SW3`.`sw_graphic`)))
                      )
                      left join `source_word` `SW4` on(((`NU`.`first_language` = `SW4`.`first_language`) and (`NU`.`survey_language` = `SW4`.`survey_language`) and (`NU`.`sw4_graphic` = `SW4`.`sw_graphic`)))
                  )
                  left join `splinter` `GS` on(((`NU`.`nu_graphic` = `GS`.`nu_graphic`) and (`NU`.`first_language` = `GS`.`first_language`) and (`NU`.`survey_language` = `GS`.`survey_language`) and (`NU`.`image_id` = `GS`.`image_id`) and (`GS`.`type_of_splinter` = 'graphic strict')))
              )
              left join `splinter` `GM` on(((`NU`.`nu_graphic` = `GM`.`nu_graphic`) and (`NU`.`first_language` = `GM`.`first_language`) and (`NU`.`survey_language` = `GM`.`survey_language`) and (`NU`.`image_id` = `GM`.`image_id`) and (`GM`.`type_of_splinter` = 'graphic modified')))
          )
          left join `splinter` `PS` on(((`NU`.`nu_graphic` = `PS`.`nu_graphic`) and (`NU`.`first_language` = `PS`.`first_language`) and (`NU`.`survey_language` = `PS`.`survey_language`) and (`NU`.`image_id` = `PS`.`image_id`) and (`PS`.`type_of_splinter` = 'phonetic strict')))
      )
      left join `splinter` `PM` on(((`NU`.`nu_graphic` = `PM`.`nu_graphic`) and (`NU`.`first_language` = `PM`.`first_language`) and (`NU`.`survey_language` = `PM`.`survey_language`) and (`NU`.`image_id` = `PM`.`image_id`) and (`PM`.`type_of_splinter` = 'phonetic modified')))
  )
"""

OLD_VIEW = """
CREATE OR REPLACE VIEW `nu_full` AS
  select
    `NU`.`nu_graphic` AS `nu_graphic`,
    `NU`.`first_language` AS `first_language`,
    `NU`.`survey_language` AS `survey_language`,
    NU.wf_process as wf_process,
    NU.wfp_specification as wfp_specification,
    NU.wfp_strict_modification as wfp_strict_modification,
    NU.connect_element as connect_element,
    `NU`.`image_id` AS `image_id`,
    `NU`.`nu_phonetic` AS `nu_phonetic`,
    `NU`.`nu_syllabic` AS `nu_syllabic`,
    `NU`.`nu_graphic_len` AS `nu_graphic_len`,
    `NU`.`nu_phonetic_len` AS `nu_phonetic_len`,
    `NU`.`nu_syllabic_len` AS `nu_syllabic_len`,
    `NU`.`sw1_graphic` AS `sw1_graphic`,
    `NU`.`sw2_graphic` AS `sw2_graphic`,
    `NU`.`sw3_graphic` AS `sw3_graphic`,
    `NU`.`sw4_graphic` AS `sw4_graphic`,
    `SW1`.`sw_word_class` AS `sw1_word_class`,
    `SW2`.`sw_word_class` AS `sw2_word_class`,
    `SW3`.`sw_word_class` AS `sw3_word_class`,
    `SW4`.`sw_word_class` AS `sw4_word_class`,
    `SW1`.`source_language` AS `sw1_source_language`,
    `SW2`.`source_language` AS `sw2_source_language`,
    `SW3`.`source_language` AS `sw3_source_language`,
    `SW4`.`source_language` AS `sw4_source_language`,
    SW1.proper_name AS sw1_proper_name,
    SW2.proper_name AS sw2_proper_name,
    SW3.proper_name AS sw3_proper_name,
    SW4.proper_name AS sw4_proper_name,
    `SW1`.`sw_graphic_len` AS `sw1_graphic_len`,
    `SW2`.`sw_graphic_len` AS `sw2_graphic_len`,
    `SW3`.`sw_graphic_len` AS `sw3_graphic_len`,
    `SW4`.`sw_graphic_len` AS `sw4_graphic_len`,
    `SW1`.`sw_phonetic` AS `sw1_phonetic`,
    `SW2`.`sw_phonetic` AS `sw2_phonetic`,
    `SW3`.`sw_phonetic` AS `sw3_phonetic`,
    `SW4`.`sw_phonetic` AS `sw4_phonetic`,
    `SW1`.`sw_phonetic_len` AS `sw1_phonetic_len`,
    `SW2`.`sw_phonetic_len` AS `sw2_phonetic_len`,
    `SW3`.`sw_phonetic_len` AS `sw3_phonetic_len`,
    `SW4`.`sw_phonetic_len` AS `sw4_phonetic_len`,
    `SW1`.`sw_syllabic` AS `sw1_syllabic`,
    `SW2`.`sw_syllabic` AS `sw2_syllabic`,
    `SW3`.`sw_syllabic` AS `sw3_syllabic`,
    `SW4`.`sw_syllabic` AS `sw4_syllabic`,
    `SW1`.`sw_syllabic_len` AS `sw1_syllabic_len`,
    `SW2`.`sw_syllabic_len` AS `sw2_syllabic_len`,
    `SW3`.`sw_syllabic_len` AS `sw3_syllabic_len`,
    `SW4`.`sw_syllabic_len` AS `sw4_syllabic_len`,
    `SW1`.`frequency_in_snc` AS `sw1_frequency_in_snc`,
    `SW2`.`frequency_in_snc` AS `sw2_frequency_in_snc`,
    `SW3`.`frequency_in_snc` AS `sw3_frequency_in_snc`,
    `SW4`.`frequency_in_snc` AS `sw4_frequency_in_snc`,
    `GS`.`type_of_splinter` AS `gs_name`,
    `GS`.`sw1_splinter` AS `gs_sw1_splinter`,
    `GS`.`sw2_splinter` AS `gs_sw2_splinter`,
    `GS`.`sw3_splinter` AS `gs_sw3_splinter`,
    `GS`.`sw4_splinter` AS `gs_sw4_splinter`,
    `GS`.`sw1_splinter_len` AS `gs_sw1_splinter_len`,
    `GS`.`sw2_splinter_len` AS `gs_sw2_splinter_len`,
    `GS`.`sw3_splinter_len` AS `gs_sw3_splinter_len`,
    `GS`.`sw4_splinter_len` AS `gs_sw4_splinter_len`,
    (`GS`.`sw1_splinter_len` / `SW1`.`sw_graphic_len`) AS `gs_sw1_splinter_len_to_sw_len`,
    (`GS`.`sw2_splinter_len` / `SW2`.`sw_graphic_len`) AS `gs_sw2_splinter_len_to_sw_len`,
    (`GS`.`sw3_splinter_len` / `SW3`.`sw_graphic_len`) AS `gs_sw3_splinter_len_to_sw_len`,
    (`GS`.`sw4_splinter_len` / `SW4`.`sw_graphic_len`) AS `gs_sw4_splinter_len_to_sw_len`,
    (`GS`.`sw1_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw1_splinter_len_to_nu_len`,
    (`GS`.`sw2_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw2_splinter_len_to_nu_len`,
    (`GS`.`sw3_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw3_splinter_len_to_nu_len`,
    (`GS`.`sw4_splinter_len` / `NU`.`nu_graphic_len`) AS `gs_sw4_splinter_len_to_nu_len`,
    `GM`.`type_of_splinter` AS `gm_name`,
    `GM`.`sw1_splinter` AS `gm_sw1_splinter`,
    `GM`.`sw2_splinter` AS `gm_sw2_splinter`,
    `GM`.`sw3_splinter` AS `gm_sw3_splinter`,
    `GM`.`sw4_splinter` AS `gm_sw4_splinter`,
    `GM`.`sw1_splinter_len` AS `gm_sw1_splinter_len`,
    `GM`.`sw2_splinter_len` AS `gm_sw2_splinter_len`,
    `GM`.`sw3_splinter_len` AS `gm_sw3_splinter_len`,
    `GM`.`sw4_splinter_len` AS `gm_sw4_splinter_len`,
    (`GM`.`sw1_splinter_len` / `SW1`.`sw_graphic_len`) AS `gm_sw1_splinter_len_to_sw_len`,
    (`GM`.`sw2_splinter_len` / `SW2`.`sw_graphic_len`) AS `gm_sw2_splinter_len_to_sw_len`,
    (`GM`.`sw3_splinter_len` / `SW3`.`sw_graphic_len`) AS `gm_sw3_splinter_len_to_sw_len`,
    (`GM`.`sw4_splinter_len` / `SW4`.`sw_graphic_len`) AS `gm_sw4_splinter_len_to_sw_len`,
    (`GM`.`sw1_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw1_splinter_len_to_nu_len`,
    (`GM`.`sw2_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw2_splinter_len_to_nu_len`,
    (`GM`.`sw3_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw3_splinter_len_to_nu_len`,
    (`GM`.`sw4_splinter_len` / `NU`.`nu_graphic_len`) AS `gm_sw4_splinter_len_to_nu_len`,
    `PS`.`type_of_splinter` AS `ps_name`,
    `PS`.`sw1_splinter` AS `ps_sw1_splinter`,
    `PS`.`sw2_splinter` AS `ps_sw2_splinter`,
    `PS`.`sw3_splinter` AS `ps_sw3_splinter`,
    `PS`.`sw4_splinter` AS `ps_sw4_splinter`,
    `PS`.`sw1_splinter_len` AS `ps_sw1_splinter_len`,
    `PS`.`sw2_splinter_len` AS `ps_sw2_splinter_len`,
    `PS`.`sw3_splinter_len` AS `ps_sw3_splinter_len`,
    `PS`.`sw4_splinter_len` AS `ps_sw4_splinter_len`,
    (`PS`.`sw1_splinter_len` / `SW1`.`sw_phonetic_len`) AS `ps_sw1_splinter_len_to_sw_len`,
    (`PS`.`sw2_splinter_len` / `SW2`.`sw_phonetic_len`) AS `ps_sw2_splinter_len_to_sw_len`,
    (`PS`.`sw3_splinter_len` / `SW3`.`sw_phonetic_len`) AS `ps_sw3_splinter_len_to_sw_len`,
    (`PS`.`sw4_splinter_len` / `SW4`.`sw_phonetic_len`) AS `ps_sw4_splinter_len_to_sw_len`,
    (`PS`.`sw1_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw1_splinter_len_to_nu_len`,
    (`PS`.`sw2_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw2_splinter_len_to_nu_len`,
    (`PS`.`sw3_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw3_splinter_len_to_nu_len`,
    (`PS`.`sw4_splinter_len` / `NU`.`nu_phonetic_len`) AS `ps_sw4_splinter_len_to_nu_len`,
    `PM`.`type_of_splinter` AS `pm_name`,
    `PM`.`sw1_splinter` AS `pm_sw1_splinter`,
    `PM`.`sw2_splinter` AS `pm_sw2_splinter`,
    `PM`.`sw3_splinter` AS `pm_sw3_splinter`,
    `PM`.`sw4_splinter` AS `pm_sw4_splinter`,
    `PM`.`sw1_splinter_len` AS `pm_sw1_splinter_len`,
    `PM`.`sw2_splinter_len` AS `pm_sw2_splinter_len`,
    `PM`.`sw3_splinter_len` AS `pm_sw3_splinter_len`,
    `PM`.`sw4_splinter_len` AS `pm_sw4_splinter_len`,
    (`PM`.`sw1_splinter_len` / `SW1`.`sw_phonetic_len`) AS `pm_sw1_splinter_len_to_sw_len`,
    (`PM`.`sw2_splinter_len` / `SW2`.`sw_phonetic_len`) AS `pm_sw2_splinter_len_to_sw_len`,
    (`PM`.`sw3_splinter_len` / `SW3`.`sw_phonetic_len`) AS `pm_sw3_splinter_len_to_sw_len`,
    (`PM`.`sw4_splinter_len` / `SW4`.`sw_phonetic_len`) AS `pm_sw4_splinter_len_to_sw_len`,
    (`PM`.`sw1_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw1_splinter_len_to_nu_len`,
    (`PM`.`sw2_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw2_splinter_len_to_nu_len`,
    (`PM`.`sw3_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw3_splinter_len_to_nu_len`,
    (`PM`.`sw4_splinter_len` / `NU`.`nu_phonetic_len`) AS `pm_sw4_splinter_len_to_nu_len`
  from (
      (
          (
              (
                  (
                      (
                          (
                              (
                                  (`naming_unit` `NU`)
                                  left join `source_word` `SW1` on(((`NU`.`first_language` = `SW1`.`first_language`) and (`NU`.`survey_language` = `SW1`.`survey_language`) and (`NU`.`sw1_graphic` = `SW1`.`sw_graphic`)))
                              )
                              left join `source_word` `SW2` on(((`NU`.`first_language` = `SW2`.`first_language`) and (`NU`.`survey_language` = `SW2`.`survey_language`) and (`NU`.`sw2_graphic` = `SW2`.`sw_graphic`)))
                          )
                          left join `source_word` `SW3` on(((`NU`.`first_language` = `SW3`.`first_language`) and (`NU`.`survey_language` = `SW3`.`survey_language`) and (`NU`.`sw3_graphic` = `SW3`.`sw_graphic`)))
                      )
                      left join `source_word` `SW4` on(((`NU`.`first_language` = `SW4`.`first_language`) and (`NU`.`survey_language` = `SW4`.`survey_language`) and (`NU`.`sw4_graphic` = `SW4`.`sw_graphic`)))
                  )
                  left join `splinter` `GS` on(((`NU`.`nu_graphic` = `GS`.`nu_graphic`) and (`NU`.`first_language` = `GS`.`first_language`) and (`NU`.`survey_language` = `GS`.`survey_language`) and (`NU`.`image_id` = `GS`.`image_id`) and (`GS`.`type_of_splinter` = 'graphic strict')))
              )
              left join `splinter` `GM` on(((`NU`.`nu_graphic` = `GM`.`nu_graphic`) and (`NU`.`first_language` = `GM`.`first_language`) and (`NU`.`survey_language` = `GM`.`survey_language`) and (`NU`.`image_id` = `GM`.`image_id`) and (`GM`.`type_of_splinter` = 'graphic modified')))
          )
          left join `splinter` `PS` on(((`NU`.`nu_graphic` = `PS`.`nu_graphic`) and (`NU`.`first_language` = `PS`.`first_language`) and (`NU`.`survey_language` = `PS`.`survey_language`) and (`NU`.`image_id` = `PS`.`image_id`) and (`PS`.`type_of_splinter` = 'phonetic strict')))
      )
      left join `splinter` `PM` on(((`NU`.`nu_graphic` = `PM`.`nu_graphic`) and (`NU`.`first_language` = `PM`.`first_language`) and (`NU`.`survey_language` = `PM`.`survey_language`) and (`NU`.`image_id` = `PM`.`image_id`) and (`PM`.`type_of_splinter` = 'phonetic modified')))
  )
"""

step(NEW_VIEW, OLD_VIEW)