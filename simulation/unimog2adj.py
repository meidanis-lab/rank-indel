#!/usr/bin/env python
"""
Input:
    1 2 -3 )
    4 )
Output:
    4_t 4_h
    1_t 3_t
    1_h 2_t
    2_h 3_h
"""

import fileinput

def get_extrs(genes):
    extrs = []
    for gene in genes:
        if gene.startswith('-'):
            extrs.extend([gene[1:] + '_h', gene[1:] + '_t'])
        else:
            extrs.extend([gene + '_t', gene + '_h'])
    return extrs

def get_adjs(extrs):
    return '\n'.join(f'{extr1} {extr2}' for extr1, extr2 in zip(extrs[1::2], extrs[2::2]))


with fileinput.input() as fin:
    for line in fin:
        line = line.strip()
        if line.endswith(')'):
            genes = line.strip(')').split()
            extrs = get_extrs(genes)
            print(extrs[0], extrs[-1])
            print(get_adjs(extrs))
        elif line.endswith(']'):
            genes = line.strip(']').split()
            extrs = get_extrs(genes)
            print(get_adjs(extrs))
        else:
            raise SystemExit('Not circular nor linear.')
