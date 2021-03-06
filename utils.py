import json

from enums import BOOLEAN, TEXT, INTEGER


def get_db_configs():
    with open('config.json') as f:
        data = json.load(f)

    return data


def get_file_type(data_file):
    return data_file.rsplit('_', 1)[0]


def get_drop_date(data_file):
    return data_file.rsplit('_', 1)[1].replace('.txt', '')


def parse_col(col, col_type):
    if col_type == BOOLEAN:
        return 'true' if col.strip() == '1' else 'false'
    elif col_type == TEXT:
        return "'{}'".format(col.strip())
    else: # INTEGER
        return col.strip()
