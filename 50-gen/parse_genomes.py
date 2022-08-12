#!/usr/bin/python3

from argparse import ArgumentParser, FileType

def construct_chromosome(chromosome):
    '''Transforms space-separated string of synteny blocks
    into space-separated string of adjacencies.
    '''
    result = []
    for synteny in chromosome.split():
        tail = synteny[1:] + '_t'
        head = synteny[1:] + '_h'
        if synteny.startswith('+'):
            result.extend([tail, head])
        elif synteny.startswith('-'):
            result.extend([head, tail])
        else:
            print(synteny)
            raise ValueError(f'{synteny} does not specify orientation: + or -')
    return result

def format(chromosomes):
    '''WARNING: ALL chromosomes are either circular or linear; current
    version does not admit genomes with mixed types of chromosomes.
    '''
    result = []
    for chromosome in chromosomes:
        first, last = None, None
        # TODO: maintain global access to args.circular?
        if args.circular:
            first, last = '(', ')'
        else:
            first, last = '[', ']'
        result.append(f'{first} {" ".join(chromosome)} {last}')
    # last \n is convenient for Linux files (e.g. wc -l counts correctly)
    return '\n'.join(result) + '\n'

DESCRIPTION = 'Read genome file and transform syntenies into adjacencies.'

parser = ArgumentParser(DESCRIPTION)
parser.add_argument('-i', '--input', required=True, type=FileType('r'), help='path for input file in genome format')
parser.add_argument('-o', '--output', type=FileType('w'), help='path for output file in gen format')
group = parser.add_mutually_exclusive_group()
group.add_argument('-l', '--linear', action='store_true', help='interpret genome as linear (DEFAULT)')
group.add_argument('-c', '--circular', action='store_true', help='interpret genome as circular')
args = parser.parse_args()

chromosomes = [construct_chromosome(line.strip()) for line in args.input]

if args.output:
    args.output.write(format(chromosomes))
else:
    print(format(chromosomes))
