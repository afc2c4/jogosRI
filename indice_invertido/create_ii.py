import os
import re
import json

inv_index = {}


def readJson(json_dict, file_index):
    for words in json_dict.values():
        if words in ['', '--']:
            continue
        words = words.strip().split(' ')
        for word in words:
            if not inv_index.get(word, False):
                aux_set = set(file_index)
                inv_index[word] = aux_set
            else:
                inv_index[word].add(file_index)


if __name__ == '__main__':
    path_db = os.path.abspath('./db')
    for file_name in os.listdir(path_db):
        file_path = path_db + '\\' + file_name
        with open(file_path, 'r', encoding='utf-8') as file:
            file_text = file.read()
            file_text = re.sub(r'\\xc2|\\xae|\\xe2|\\x80|\\x99|\\x84|\\xa2|\\x93|\\xa0|\\', '', file_text)
            json_dict = json.loads(file_text[:-1])
        readJson(json_dict, file_name)
    print(inv_index)


