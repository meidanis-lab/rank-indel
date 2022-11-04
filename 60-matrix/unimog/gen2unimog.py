#!/usr/bin/env python

## TODO: replace by simpler script

import fileinput

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

fmt_genome_name = lambda path: path.split('/')[-1].split('.')[0]
print('>' + fmt_genome_name(fin.filename()) + '\n' + '\n'.join(genome))
