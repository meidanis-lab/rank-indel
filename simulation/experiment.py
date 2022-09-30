#!/usr/bin/env python

import itertools
import sys
import subprocess
import shutil
import tqdm

if len(sys.argv) != 3:
    raise SystemExit('usage: ./experiment.py [parameters file] [number of iterations]')

with open(sys.argv[1], 'r') as fin:
    params = dict()
    for line in fin:
        k, *v = line.strip().split()
        params[k] = v

niters = int(sys.argv[2])

for k, conf in enumerate(itertools.product(*params.values())):
    # be careful with the ordering
    g, x, i, e, zipf = conf
    for j in tqdm.tqdm(range(niters), ascii=' #'):
        try:
            subprocess.check_output(f'make rank_tree NGENES={g} NCHRS={x} INSERTION_RATE={i} DELETION_RATE={e} INDEL_SIZE={zipf} -B', shell=True)
            shutil.move('rank/rank_tree.nwk', f'rank/rank_tree_conf{k}_iter{j}.nwk')
        except subprocess.CalledProcessError as e:
            print(e.output, e.returncode)
