import csv
import os
import sys

from itertools import islice

def read_csv_spec(data_file, header=True):
    # TODO add tests
    spec_file = '{}.csv'.format(data_file.rsplit('_', 1)[0])

    try:
        with open(os.path.join('specs', spec_file), 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for r in islice(csv_reader, 1 if header else 0, None):
                yield r
    except IOError as e:
        print 'No csv spec file {} found for data file {}'.format(spec_file, data_file)


def read_data(data_file):
    for row in read_csv_spec(data_file):
        print row

if __name__ == '__main__':
    map(read_data, sys.argv[1:])
