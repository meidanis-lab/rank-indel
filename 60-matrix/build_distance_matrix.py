#!/usr/bin/env python3
'''This script converts a CSV file contaning two genomes and their distance per line
into a lower triangular distance matrix.
'''

import fileinput
import csv
import sys
from collections import defaultdict

if len(sys.argv) < 2:
    raise SystemExit('need to pass a CSV file')
elif len(sys.argv) > 2:
    raise SystemExit('only one argument expected')
else:
    with fileinput.input() as fin:
        matrix = defaultdict(dict)
        for line in csv.reader(fin):
            matrix[line[0]][line[1]] = line[2]
            matrix[line[1]][line[0]] = line[2]

    labels = sorted(matrix)
    print(',' + ','.join(labels))
    for row in labels:
        curr_row = []
        repeated = False
        for col in labels:
            if row in matrix[col] and not repeated:
                curr_row.append(matrix[col][row])
            else:
                curr_row.append('')
                repeated = True
        curr_row = ','.join(curr_row)
        print(row, curr_row, sep=',')
