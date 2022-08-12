#!/usr/bin/python3

from sys import argv
from itertools import combinations
from os import path, listdir

gen_dir = argv[1]
if not path.isdir(gen_dir):
    print(f'{gen_dir} not a directory')
    exit(1)

is_concatenated_adj_file = lambda f: len(f.split('-')) == 2
genomes = [fname for fname in listdir(gen_dir) if is_concatenated_adj_file(fname)]

for i,j in combinations(genomes, 2):
    print(f'{gen_dir}/{i}\t{gen_dir}/{j}')
