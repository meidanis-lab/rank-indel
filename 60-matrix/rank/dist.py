#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""dist.py
   computes rank and rank-indel distances between genomes
   input: given as two files, whose names appear in the command line
          format of the files: lines of the form
          g1_k1 g2_k2
          where g1 is the name of gene 1 and k1 is it kind, which can be
          'h' ot 't' meaning head or tail, and similarly for the other extremity.
          genes can be missing from one of the genomes, but cannot be duplicated
          in the same genome.
   output: the rank and rank-indel distances, according to:
          Zanetti, Chindelevitch, Meidanis, "Rank distance generalizations
          for genomes with indels", 2018.
"""

import sys
import dsuf

def usage():
    print('Usage: {0} genome1 genome2 diag'.format(sys.argv[0]), file=sys.stderr)
    print('  where each genome file contains lines with pairs of extremities, e.g', file=sys.stderr)
    print('  gene1_t gene3_h', file=sys.stderr)
    print('  abd diag is a diagnostics flag (diag=0: no msgs)', file=sys.stderr)

def readGenome(filename, charge, ds, diag):
    genes = {}
    edges = []
    with open(filename, 'r') as f1:
        lines = 0
        for line in f1:
            lines += 1
            ## split to find extremities
            extrs = line.split()
            ## then split extremity to find gene
            for extr in extrs:
                gene = extr[:-2]
                if gene not in genes:
                    genes[gene] = 1
            ## save for later
            edges.append(extrs)
    for gene in genes:
        ds.find(gene + '_h', charge)
        ds.find(gene + '_t', charge)
    return genes, edges

def processGenome(edges, ds, diag):
    for extrs in edges:
        ds.union(extrs[0], extrs[1])

if len(sys.argv) <= 3:
    usage()
    exit(1)

diag = int(sys.argv[1])
indl = int(sys.argv[2])
genome1 = sys.argv[3]
genome2 = sys.argv[4]

##################################################
### read genomes and initialize components
ds = dsuf.DSCollection()

### read genome 1
(genes1, edges1) = readGenome(genome1, +1, ds, diag)

### print summary of genome1
### number of genes
#print('Genome 1:')
#print('  genes: {0}'.format(len(genes1)))

(genes2, edges2) = readGenome(genome2, -1, ds, diag)

### print summary of genome2
### number of genes
#print('Genome 2:')
#print('  genes: {0}'.format(len(genes2)))

### print summary of both genomes
### number of genes
genes = set(genes1) | set(genes2)
#print('Both Genomes:')
#print('  genes: {0}'.format(len(genes)))

##################################################
### process genome edges
processGenome(edges1, ds, diag)
processGenome(edges2, ds, diag)

##################################################
### compute distances
n = len(genes)
c = 0
p0 = 0
p12 = 0
for ci in ds.comp:
    if ci.cycle():
        c = c + 1
    elif ci.term1.charge == 0 and ci.term2.charge == 0:
        p0 = p0 + 1
    elif ci.term1.charge + ci.term2.charge == 0:
        p12 = p12 + 1

extract_name = lambda infile: infile.split('/')[-1].split('.')[0]

if indl >= 1:
    print(f'{extract_name(genome1)}\t{extract_name(genome2)}\t{2*n - 2*c - p0 + p12}') # rank indl
else:
    print(f'{extract_name(genome1)}\t{extract_name(genome2)}\t{2*n - 2*c - p0 - p12}') # rank dist

if diag >= 1:
    print(f'c {c} p0 {p0} p12 {p12}\n')
