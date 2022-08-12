#!/usr/bin/env python3

from itertools import combinations
from sys import argv

files = [fname for fname in argv[1:]]
for i, j in combinations(files, 2):
    print(f"{i}\t{j}")
