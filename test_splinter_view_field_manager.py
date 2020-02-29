from src.splinter_view_field_manager import SplinterViewFieldManager

NU_FIELDS = (
        'nu_graphic', 'first_language', 'survey_language', 'image_id',
        'wf_process',
        'nu_word_class', 'nu_phonetic',
        'nu_syllabic',
        'nu_graphic_len',
        'nu_phonetic_len',
        'nu_syllabic_len',
        'n_of_overlapping_letters',
        'n_of_overlapping_phones',
        'lexsh_main', 'lexsh_sm', 'lexsh_whatm',
        'split_point_1', 'split_point_2', 'split_point_3',
    )

IMG_FIELDS = (
        'sub_sem_cat', 'dom_sem_cat', 'sub_name', 'dom_name',
        'sub_number', 'dom_number', 'half_number', 'sub_sub'
    )

SW_FIELDS = (
        'sw_graphic', 'source_language',
        'sw_phonetic', 'sw_word_class', 'sw_syllabic',
        'sw_graphic_len', 'sw_phonetic_len', 'sw_syllabic_len',
    )

SPL_FIELDS = (
        'type_of_splinter',
        'sw1_splinter', 'sw2_splinter', 'sw3_splinter', 'sw4_splinter',
        'sw1_splinter_len', 'sw2_splinter_len', 'sw3_splinter_len', 'sw4_splinter_len',
        'G_sw1_splinter', 'G_sw1_splinter__ignore', 'G_sw2_splinter', 'G_sw2_splinter__ignore',
        'G_sw3_splinter', 'G_sw3_splinter__ignore', 'G_sw4_splinter', 'G_sw4_splinter__ignore',
        'G_sw1_splinter_len', 'G_sw1_splinter_len__ignore', 'G_sw2_splinter_len', 'G_sw2_splinter_len__ignore',
        'G_sw3_splinter_len', 'G_sw3_splinter_len__ignore', 'G_sw4_splinter_len', 'G_sw4_splinter_len__ignore'
    )

SPL_TYPES = ('gs', 'gm', 'ps', 'pm')

if __name__ == '__main__':

    obj = SplinterViewFieldManager(NU_FIELDS, IMG_FIELDS, SW_FIELDS, SPL_FIELDS, SPL_TYPES)

    print('Select fields:')
    for f in obj.select_fields:
        print(f)
    print()

    print('Flat fields:')
    for f in obj.flat_fields:
        print(f)
    print()

    print('Static fields:')
    for f in obj.static_fields:
        print(f)
    print()

    print('G_gm_sw3_splinter__ignore', '<->', obj.current_to_original['G_gm_sw3_splinter__ignore'])
    print('ps_name', '<->', obj.current_to_original['ps_name'])
    print('sw4_phonetic_len', '<->', obj.current_to_original['sw4_phonetic_len'])




