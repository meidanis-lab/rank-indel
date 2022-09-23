#!/usr/bin/env python

import fileinput
from itertools import combinations

with fileinput.input() as fin:
    genomes = dict()
    curr = None
    for line in fin:
        if line.startswith('>'):
            curr = line.strip()
            genomes[curr] = []
        else:
            genomes[curr].append(line.strip())

for i, j in combinations(genomes, 2):
    output = f'{i[1:]}_vs_{j[1:]}.unimog'
    with open(output, 'w') as fout:
        fout.write(i + '\n')
        fout.write('\n'.join(genomes[i]) + '\n')
        fout.write(j + '\n')
        fout.write('\n'.join(genomes[j]) + '\n')
