#!/usr/bin/env python
"""
Usage:
 $ {} <directory>
 $ {} <file1> <file2> ...
"""

from __future__ import print_function

import csv
import logging
import os
import psycopg2
import sys

from itertools import islice
from enums import BOOLEAN, INTEGER, TEXT, DATA_LOADED_TABLE, DROP_DATE_COLUMN
from utils import get_db_configs, get_file_type, get_drop_date, parse_col


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('data_loader')

db_configs = get_db_configs()
conn = psycopg2.connect(**db_configs)
cur = conn.cursor()


def is_loaded(data_file):
    cur.execute("SELECT * FROM {} where data_file = '{}'".format(DATA_LOADED_TABLE, data_file))
    return bool(cur.fetchone())


def mark_loaded(data_file):
    cur.execute("INSERT INTO {} values ('{}', now())".format(DATA_LOADED_TABLE, data_file))
    return None


def read_csv_spec(data_file, header=True):
    spec_file = '{}.csv'.format(get_file_type(data_file))

    try:
        with open(os.path.join('specs', spec_file), 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            return list(islice(csv_reader, 1 if header else 0, None))
    except IOError as e:
        logger.error('No csv spec file "{}" found for data file "{}", skipping...'.format(spec_file, data_file))

    return None


def create_table(table_name, fields):
    columns = ['{} DATE'.format(DROP_DATE_COLUMN)]
    columns += [' '.join([field[0].replace(' ', '_'), field[2]]) for field in fields]

    cur.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, ', '.join(columns)))
    return None


def insert_line(table_name, drop_date, line, fields):
    i = 0
    values = ["'{}'".format(drop_date)]
    for field in fields:
        col_width = int(field[1])
        values.append(parse_col(line[i:i + col_width], field))
        i += col_width

    cur.execute('INSERT INTO {} values ({})'.format(table_name, ', '.join(values)))
    return None


def read_data(data_file, fields):
    table_name = get_file_type(data_file)
    drop_date = get_drop_date(data_file)
    try:
        with open(os.path.join('data', data_file), 'r') as f:
            create_table(table_name, fields)
            for line in f:
                insert_line(table_name, drop_date, line.strip(), fields)
            mark_loaded(data_file)
    except IOError as e:
        logger.error('No data file "{}" found, skipping...'.format(data_file))
        return None
    except Exception as e:
        # rollback transaction and skip
        conn.rollback()
        logger.error('Error for "{}": {}'.format(data_file, e))
        return None


    try:
        # commit single transaction of table creation and insertions
        conn.commit()
        logger.info('SUCCESS loading data for "{}"'.format(data_file))
    except:
        logger.error('Transaction commit failed for "{}", skipping...'.format(data_file))

    return None


def load_data(file_path):
    data_file = os.path.basename(file_path)

    if is_loaded(data_file):
        logger.warn('Already loaded data file "{}", skipping...'.format(data_file))
        return None

    fields = read_csv_spec(data_file)

    if fields:
        read_data(data_file, fields)

    return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__.format(sys.argv[0], sys.argv[0]))
    else:
        try:
            files = os.listdir(sys.argv[1])
        except:
            files = sys.argv[1:]

        for f in files:
            load_data(f)
