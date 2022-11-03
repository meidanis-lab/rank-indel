#!/usr/bin/env python

import itertools
import sys
import subprocess
import shutil

if len(sys.argv) != 4:
    raise SystemExit('usage: ./experiment.py [distance model: rank | rankindl | dcj] [parameters file] [number of iterations]')

if sys.argv[1] not in {'rank', 'rankindl', 'dcj'}:
    raise SystemExit('Invalid distance model: must be either \'dcj\', \'rank\', or \'rankindl\'')

with open(sys.argv[2], 'r') as fin:
    params = []
    for line in fin:
        line = line.strip()
        if line and not line.startswith('#'):
            # 1st: parameter name; 2nd: low value; 3rd: high value e.g. 'g 5000 10000'
            k, low, high = line.split()
            param = dict()
            param[k.lower()] = low
            param[k.upper()] = high
            params.append(param)

niters = int(sys.argv[3])
dist = sys.argv[1]

for keys in itertools.product(*params):
    conf = ''.join(keys)
    print(f'Running configuration {conf}')

    # WARNING: an ordering is expected in params, and, therefore, in the conf file!
    g, x, i, e, z = [d[k] for k, d in zip(keys, params)]

    for j in range(niters):
        print(f'Iteration {j+1}')
        try:
            cmd = f'make -B {dist} NGENES={g} NCHRS={x} INSRATE={i} DELRATE={e} INDEL_SIZE={z}'
            print(cmd)
            subprocess.check_output(cmd, shell=True)
            shutil.move(f'{dist}/{dist}_tree.nwk', f'{dist}/{dist}_tree_{conf}_iter{j+1}.nwk')
        except subprocess.CalledProcessError as e:
            print(e.output, e.returncode)
