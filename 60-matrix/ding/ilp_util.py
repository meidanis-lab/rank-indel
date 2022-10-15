# Auxiliary functions needed by different scripts of the DCJIdDup ILP processing,
# as well as for adapting Mcd/mcdmm+ to the UniMoG format.

CHR_CIRCULAR = ')'
CHR_LINEAR = '|'
ORIENT_POSITIVE = '+'
ORIENT_NEGATIVE = '-'
EXTREMITY_TAIL = 't'
EXTREMITY_HEAD = 'h'
EXTREMITY_TELOMERE = '$'
#all telomeres are equivalent concerning the distance
TELOMERE_ID = -1

#TODO: protect for parallel execution
class Simple_Id_Generator:
    last = 0
    def get_new(self):
        self.last+=1
        return self.last

def readGenomes(data, genomesOnly=None):
    """Read genome in UniMoG format
    (https://bibiserv.cebitec.uni-bielefeld.de/dcj?id=dcj_manual)"""

    res = list()

    # helper function for parsing each individual gene
    str2gene = lambda x: x.startswith(ORIENT_NEGATIVE) and (ORIENT_NEGATIVE, \
            x[1:]) or (ORIENT_POSITIVE, x.lstrip(ORIENT_POSITIVE))
    # process each line, assuming that the file is well-formatted
    skip = False
    for line in data:
        line = line.strip()
        if line:
            if line.startswith('>'):
                genomeName = line[1:].strip()
                if genomesOnly == None or genomeName in genomesOnly:
                    skip = False
                    res.append((genomeName, list()))
                elif genomesOnly:
                    skip = True
            elif line[-1] not in (CHR_CIRCULAR, CHR_LINEAR):

                raise Exception, 'Invalid format, expected chromosome to ' + \
                        'end with either \'%s\' or \'%s\'' %(CHR_CIRCULAR, \
                        CHR_LINEAR)
            elif not skip:
                res[-1][1].append((line[-1], map(str2gene, line[:-1].split())))
    return res

def print_id_genome_unimog(genome, handle, id_pos=2):
    ''' Print a genome of format [(lin/circ, [(orient,..,id)])] to the UniMoG
        format, where id_pos conveis the position of the marker id.
    '''
    handle.write(">%s\n"%genome[0])
    for chr in genome[1]:
        for gene in chr[1]:
            orient = gene[0]
            id = gene[id_pos]
            if orient == ORIENT_NEGATIVE:
                handle.write(ORIENT_NEGATIVE)
            handle.write("%s "%str(id))
        if chr[0]!=CHR_LINEAR and chr[0] != CHR_CIRCULAR:
            raise Exception, "Internally inconsistent chromosome ending with %s!"%chr[0]
        handle.write("%s\n"%chr[0])


def concatenate_chromosome(chr):
    ''' Concatenate a chromosome in list form (lin/circ, [(orient, id)]) to
        the old internal format used by mcd: (o) orientid ... (-o) (if linear).
    '''
    front = 'o '
    back = ' -o'
    if chr[0] == CHR_LINEAR:
        front = 'o '
        back =' -o'
    chr = chr[1]
    fix = lambda x: "" if x==ORIENT_POSITIVE else x
    to_str = lambda x: "%s%s"%(fix(x[0]),x[1])
    ret = to_str(chr[0])
    del chr[0]
    for x in chr:
        ret+=" %s"%to_str(x)
    return front+ret+back

#adapter for mcd(mmplus) to read unimog genomes
def readGenomesAdapter(genomes_files):
    '''Reads an unimog file into a series of LINEAR chromosomes regardless of circular chromosomes
    INCLUDES PADDING!
    '''
    all = []
    for genomes_file in genomes_files:
        genomes = []
        with open(genomes_file) as f:
            content = f.readlines()
            gnms = readGenomes(content)
            genomes = map(lambda x: map(concatenate_chromosome ,x[1]), gnms)
            for i in range(0,len(genomes[0]) - len(genomes[1])):
                genomes[1].append('o -o')
            for i in range(0, len(genomes[1]) - len(genomes[0])):
                genomes[0].append('o -o')
    #LOG.debug('genomes: %s' %genomes)
    return genomes#, multip_genomes
