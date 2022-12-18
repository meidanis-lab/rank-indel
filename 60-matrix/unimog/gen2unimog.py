#!/usr/bin/env python

## TODO: replace by simpler script

import fileinput

def suffix(ident):
    return ident.split('_')[-1][:6]

def prefix(ident):
    return ident[0] + ident[2].upper()

def get_organism(path):
    return path.split('/')[-1].split('.')[0]

## for PHYLIP, identifier must have exactly 10 characters
## we adopt the following convention: E_coli_123456789 ==> Ec12345678
## that is, one upper letter for genus, one upper letter for species, and 8 letters for PREFIX of strain
def fmt_ident(organism):
    return prefix(organism) + '_' + suffix(organism)

with fileinput.input() as fin:
    genome = []
    for line in fin:
        chrom = []
        for ch in line.strip("()[] \n").split()[::2]:
            if ch.endswith('t'):
                chrom.append(ch[:-2])
            elif ch.endswith('h'):
                chrom.append('-' + ch[:-2])
        if line.strip().endswith(')'):
            chrom.append(')')
        elif line.strip().endswith(']'):
            chrom.append('|')
        genome.append(' '.join(chrom))

print('>' + fmt_ident(get_organism(fin.filename())) + '\n' + '\n'.join(genome))
