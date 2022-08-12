#!/usr/bin/env python

import os
import sys
import random
import re
import argparse
import copy

DESCRIPTION = '''
Randomly removes (#genes * r) of genes from all genomes passed as input.
Among these genes, the intersection of genes present in all genomes is
fixed to be removed; the remaining genes are chosen randomly.
Repeat i=0..n-1 times and output results in samples/i.

Example:
    $ ./jackknife.py -i genome_01.genome,genome_02.genome -r .75 -n 100

We suggest using 'paste' and 'xargs' in conjuction when using this tool in a pipe.
For example, suppose there is a text file 'genomes.txt' containing all genome files
line by line. Then, we could run jackknife as follows:
    $ cat genomes.txt | paste -s -d, | xargs -I {} ./jackknife.py -i {}
'''
OUTPUT_DIR = 'samples'

def get_parser():
    parser = argparse.ArgumentParser(
            description=DESCRIPTION,
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
            '-i', '--input',
            type=str,
            help='comma-separated list of genome files')
    parser.add_argument(
            '-n', '--number-samples',
            nargs='?',
            const=1,
            type=int,
            default=50,
            help='number of samples/replicates to be generated (default: 50)')
    parser.add_argument(
            '-r', '--rate',
            nargs='?',
            const=1,
            type=float,
            default=0.5,
            help='value in [0.0,1.0] for jackknife rate (default: 0.5)')
    return parser

def get_genes(genome):
    return set(re.sub(r'[+-]', '', genome).split())

def remove_random_genes(genome, rate, genes_to_remove=None):
    '''Removes (#genes in genome * rate) from genome at random. If a set of genes_to_remove is passed,
    these are removed and counted in the total percenage of genes to delete from genome. That is, after
    the genes in genes_to_remove are deleted from genome, we remove more genes a random until a total of
    (#genes in genome * rate) genes are deleted.

    Keyword arguments:
    genome -- string of gene orders.
    rate -- float between 0.0 and 1.0 specifying percetange of genes to remove from genome.
    genes_to_remove -- set of genes to remove from genome; must not be > than (#genes in genome * rate). (default: None)
    '''
    genes = get_genes(genome)
    total_genes_to_remove = int(len(genes) * rate)

    if genes_to_remove:
        genes_to_remove = copy.deepcopy(genes_to_remove)
        if (number_genes_left := total_genes_to_remove - len(genes_to_remove)) >= 0:
            remaining_genes = random.sample(list(genes - genes_to_remove), number_genes_left)
            genes_to_remove.update(remaining_genes)
    else:
        genes_to_remove = set(random.sample(list(genes), total_genes_to_remove))

    for gene in genes:
        if gene in genes_to_remove:
            regex_genes_in_middle = r'[+-]' + re.escape(gene) + r'[^\S\n]'
            genome = re.sub(regex_genes_in_middle, '', genome)
            regex_gene_at_end = r'[+-]' + re.escape(gene) + r'\n'
            genome = re.sub(regex_gene_at_end, '\n', genome)
    return genome

def get_sets_of_genes(genomes):
    return [get_genes(genome) for genome in genomes]

if __name__ == '__main__':
    from tqdm import tqdm

    parser = get_parser()
    args = parser.parse_args()

    if not args.input:
        parser.print_help(sys.stderr)
        sys.exit(1)

    infiles = args.input.split(',')

    if '' in infiles:
        sys.stderr.write('Invalid input: there is at least 1 comma not separating files\n')
        sys.exit(1)
    elif any(infile for infile in infiles if not infile.endswith('.genome')):
        sys.stderr.write('Invalid input: some file does not have .genome extension\n')
        sys.exit(1)
    else:
        genomes = dict()
        for infile in infiles:
            with open(infile, 'r') as fi:
                genomes[infile] = fi.read()

        sets_of_genes = get_sets_of_genes(genomes.values())

        # For now, always remove genes in intersection.
        # Later on, can be passed as an option in cli.
        # common_genes = set.intersection(*sets_of_genes)

        # loop goes from 1 through n+1 for better manipulations of output directories later on
        for i in tqdm(range(1, args.number_samples+1)):
            os.makedirs(f'{OUTPUT_DIR}/{i}')

            for filename, genome in genomes.items():
                outfile = f'{OUTPUT_DIR}/{i}/' + filename.split('/')[-1]
                with open(outfile, 'w') as fo:
                    # fo.write(remove_random_genes(genome, args.rate, common_genes))
                    fo.write(remove_random_genes(genome, args.rate))
