#!/home/lucas/miniconda3/envs/dcj/bin/python

import xml.etree.ElementTree as ET
from ilp_util import *
from argparse import ArgumentParser
import sys

GENE = 0
GENOME = 1
EXTREMITY = 2
DELETE = -1

def insert(pos, ins, d):
    ''' Insert gene ins at position pos into dictionary d, while dealing with the
        edge cases of circular singletons etc.
    '''
    if d.get(pos, ins) == ins:
        d[pos] = ins
        return
    #spurious case of circular singleton
    if d[pos]==DELETE:
        d[pos] = ins
        return
    if ins == DELETE:
        return
    raise Exception, "Inconsistent markers: %s assigned to %s and %s"%(pos, d[pos], ins)

def assign_markers(sol_filename):
    ''' Extract the matching as well as some distance stats from the given
        gurobi solution file.
    '''
    max_val = None
    assign = {}
    vertices = 0
    indels = 0
    telomeres = 0
    z_sum = 0
    jumps = 0
    with open(sol_filename) as fl:
        for line in fl:
            if line.startswith("# Objective value"):
                if max_val != None:
                    print("Double maximum values!!!")
                max_val = int(line.split("=")[1])
                continue
            if line.startswith("#"):
                continue
            nv = line.split(" ")
            name = nv[0]
            val = nv[1]
            if name.startswith('z'):
                z_sum+=round(float(val))
            if name.startswith('delta_r'):
                jumps+=round(float(val))
            if name.startswith('x') and (round(float(val))==1):
                exts = name.split('(')[1].split(')')[0].split(',')
                #print(exts)
                v1 = exts[0].split('_')
                v2 = exts[1].split('_')
                if v1[EXTREMITY] == EXTREMITY_TELOMERE and v1[GENOME] != v2[GENOME]:
                    telomeres+=2
                if v1[GENE] == v2[GENE] :
                    insert(v1[GENE],DELETE,assign)
                    indels+=1
                if v1[GENOME] != v2[GENOME]:
                    vertices+=2
                    insert(v1[GENE],v2[GENE],assign)
                    insert(v2[GENE],v1[GENE],assign)
    return assign, max_val,z_sum, jumps, vertices, indels, telomeres, "N/A"

def rename_genes_g(genomes, assgns, gen):
    ''' Rename the uniquely labeled genes of both genomes by new identifiers
        resulting from the matching (assgns).
    '''
    new_ids = {}
    return map(lambda (name, chrs): (name, rename_genes_c(chrs, assgns, new_ids, gen)), genomes)

def rename_genes_c(chrs, assgns, new_ids, gen):
    ''' Rename the uniquely labeled genes of one genome by new identifiers
        resulting from the matching (assgns). new_ids are the identifiers
        already in use from possibly the other genome.
    '''
    return map(lambda (kind, chr): (kind, rename_genes(chr, assgns, new_ids, gen)), chrs)

def rename_genes(chr, assgns, new_ids, gen):
    ''' Rename the uniquely labeled genes of a chromosome by new identifiers
        resulting from the matching (assgns). new_ids are the identifiers
        already in use from possibly another chromosome.
    '''
    ret = []
    for orient, id in chr:
        if not id in assgns:
            raise Exception, "No assignment for Gene %s made!"%id
        other = assgns[id]
        if other == DELETE:
            ret.append((orient,'x_%d'%gen.get_new()))
        elif other in new_ids:
            ret.append((orient, new_ids[other]))
        else:
            #print(new_ids,id)
            new_ids[id] = gen.get_new()
            ret.append((orient, new_ids[id]))
    return ret


def main():
    parser = ArgumentParser(description= 'Read a gurobi solution as well as the uniquely labeled UniMoG file to compute a distance output and equivalent genomes, which do not contain duplicates.')
    parser.add_argument('-i', nargs=1, required=True, help='gurobi solution file with a single solution to read from.')
    parser.add_argument('-u', nargs=1, required=True, help='UniMoG unique Id file to read genomes from.')
    parser.add_argument('-o', nargs=1, required=True, help='Output file for new, equivalent (according to the gurobi opimization performed) genomes without duplications.')
    parser.add_argument('-d', nargs=1, help='Distance output file')
    parser.add_argument('-g', nargs=1, type=int, help='Assumed number of Non-Deletion Markers for computing the DCJ distance if the number of genes shall not be deduced from the graph.')
    parser.add_argument('--noheader', action="store_true", help="Repress print of explanatory header.")
    args = parser.parse_args()
    assgns, max_val, z_sum, jumps, vertices, indels, telomeres, status = assign_markers(args.i[0])
    #print(assgns)
    genes = vertices/4
    if args.g:
        genes = args.g[0]
    distance = genes - max_val/2
    genomes = []
    with open(args.u[0]) as genome_file:
        genomes = readGenomes(genome_file)
    gen = Simple_Id_Generator()
    genomes = rename_genes_g(genomes, assgns, gen)
    with open(args.o[0], "w") as outfile:
        print_id_genome_unimog(genomes[0],outfile,id_pos=1)
        print_id_genome_unimog(genomes[1],outfile,id_pos=1)
    if args.d:
        distfile = open(args.d[0], "w")
    else:
        distfile = sys.stdout
    if not args.noheader:
           distfile.write("Solution-Type\t#Non-Deletion-Markers(+Telomere-Pairs)\tDistance\n")
    distfile.write("%s\t%d\t%d\n"%(status,genes,distance))

main()
