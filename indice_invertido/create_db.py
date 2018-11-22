from wrapper import wrappers as w
import json
import re
import os


def save_files(filename, attrs, index):
    filename = filename.replace('.html', '')
    with open('db/' + str(index), 'w', encoding='utf-8') as fp:
        json_text = json.dumps(attrs, ensure_ascii=False).encode('utf-8')
        fp.write(str(json_text)[2:])


def get_attrs(file_path, index):
    file_attr = w.get_atributes_steam(file_path)
    save_files(filename, file_attr, index)

if __name__ == '__main__':
    pages_path = os.path.abspath('../pages')
    pages_path += '\\'
    index = 1
    for filename in os.listdir(pages_path):
        file_path = pages_path+filename
        # Search in steam pages
        if re.match('steam', filename):
            get_attrs(file_path, index)
            index += 1
