#!/usr/bin/python3

from csv import reader
from collections import defaultdict
from sys import argv, stdin

if argv[1] == '-':
    # split each line by blank character
    infile = [line.split() for line in stdin.read().splitlines()]
else:
    infile = reader(argv[1])

matrix = defaultdict(dict)
for line in infile:
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
