from typing import List

from tools.storage import DatabaseStorage


# Tato funkcia vykonava spolocnu funkcionalitu pre sekvencny preload.
def sequential_preload_common(data: List[str], storage: DatabaseStorage, get_value_lambda):
    loaded_keys = storage.data_keys
    already_loaded_num = 0
    to_load_now: List[str] = []
    for word in data:
        if word in loaded_keys:
            already_loaded_num += 1
        else:
            to_load_now.append(word)

    print('Input words:', len(data), sep='\t')
    print('Already loaded:', already_loaded_num, sep='\t')
    print('To load now:', len(to_load_now), sep='\t')

    for i, word in enumerate(to_load_now, 1):
        value = get_value_lambda(word)
        print(i, word, value, sep='\t')
