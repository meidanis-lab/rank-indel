#!/usr/bin/env python3

import argparse

DESCRIPTION = '''
Transforms a set of genome files into a single unimog file. A typical pipeline 
computes the rearrangement distance between pairs of genomes. For instance, if 
we have two genomes files, A.genome and B.genome, we would make a unimog file 
as follows.
    $ ./genome2unimog.py -i A.genome B.genome -o A_vs_B.unimog
'''

def get_parser():
    parser = argparse.ArgumentParser(
            description=DESCRIPTION,
            formatter_class=argparse.RawTextHelpFormatter)
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument(
            '-i', '--input', 
            type=str, 
            nargs='+',
            required=True,
            help='genome(s) file(s) contaning one chromosome per line')
    required_args.add_argument(
            '-o', '--output',
            type=str,
            required=True,
            help='unimog output file')
    return parser

if __name__ == '__main__':
    format_genome_id = lambda infile: '_'.join(infile.split('/')[-1].split('.')[:-1])

    parser = get_parser()
    args = parser.parse_args()
    
    with open(args.output, 'w') as outfile:
        for genome_file in args.input:
            with open(genome_file, 'r') as infile:
                outfile.write('>' + format_genome_id(genome_file) + '\n')
                for line in infile:
                    # TODO: we assume all chromosomes are circular; to fix this, a bigger problem must be solved.
                    # Problem: 
                    #   At step 45-jackknife, we have the gene orders required for the unimog file, but not the
                    #       type of chromosome;
                    #   At step 50-gen, we parse the genome files to gen files. We specify the type of chromosome 
                    #       (circular or linear) at this stage, but the output consists of the adjacencies;
                    #   We need the gene orders AND the type of chromosome to make an unimig file. Probably, we
                    #       should specify the type of chromosome earlier in the pipeline and remove this feature
                    #       from the parse_genome.py script in 50-gen.
                    outfile.write(line.strip().replace('+', '') + ' )' + '\n')
