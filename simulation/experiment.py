#!/usr/bin/env python

import itertools
import sys
import subprocess
import shutil
import tqdm

if len(sys.argv) != 3:
    raise SystemExit('usage: ./experiment.py [parameters file] [number of iterations]')

with open(sys.argv[1], 'r') as fin:
    params = []
    for line in fin:
        line = line.strip()
        if line and not line.startswith('#'):
            # 1st: parameter name; 2nd: low value; 3rd: high value
            # e.g. 'g 5000 10000'
            k, low, high = line.split()
            param = dict()
            param[k.lower()] = low
            param[k.upper()] = high
            params.append(param)

niters = int(sys.argv[2])

for keys in tqdm.tqdm(itertools.product(*params), ascii=' #'):
    conf = ''.join(keys)

    # WARNING: an ordering is expected in params, and, therefore, 
    # in the conf file!
    g, x, i, e, z = [d[k] for k, d in zip(keys, params)]

    for j in range(niters):
        try:
            subprocess.check_output(f'make rank_tree NGENES={g} NCHRS={x} INSERTION_RATE={i} DELETION_RATE={e} INDEL_SIZE={z} -B', shell=True)
            shutil.move('rank/rank_tree.nwk', f'rank/rank_tree_{conf}_iter{j+1}.nwk')
        except subprocess.CalledProcessError as e:
            print(e.output, e.returncode)
