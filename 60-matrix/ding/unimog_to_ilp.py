#!~/miniconda3/envs/dcj/bin/python

import sys
from ilp_util import *
from argparse import ArgumentParser
import argparse
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

NO_RANGE = 'NR'
genome1 = 'A'
genome2 = 'B'

#for catching the (rare) edge cases, that an edge belongs to a circular chromosome
singleton_circulars = []
class ADJ_Vertex:
    vertex_id = -1
    extremity = EXTREMITY_HEAD
    gene_id = 0
    genome_id = -1
    def __init__(self, v_id, ext, gene_id, genome_id):
        self.vertex_id = v_id
        self.gene_id = gene_id
        self.genome_id = genome_id
        if not ext in [EXTREMITY_HEAD,EXTREMITY_TAIL,EXTREMITY_TELOMERE]:
            raise Exception, 'Invalid extremity "%s" assigned to vertex!'%ext
        self.extremity = ext
    def get_i(self):
        d=0
        if self.extremity == EXTREMITY_HEAD:
            d=1
        if self.extremity == EXTREMITY_TAIL:
            d=2
        return 3*self.vertex_id+d

class g_Edge:
    vertex1 = 0
    vertex2 = 0
    #auxiliary variable for the (unlikely) case of a singleton circular chromosome
    can_be_self = True
    def __init__(self, v1, v2):
        self.vertex1 = v1
        self.vertex2 = v2
    def is_self(self):
        return self.can_be_self and (self.vertex1.vertex_id == self.vertex2.vertex_id)
    def is_adjacency(self):
        return (not self.is_self()) and (not self.is_cross_genome())
    def is_cross_genome(self):
        return self.vertex1.genome_id != self.vertex2.genome_id
    def repress_self(self):
        self.can_be_self = False

class ILP:
    variables = []
    maximization_function = []
    conditions = []

class ILP_variable:
    Id = 0
    rangemin = 0
    rangemax = 1
    def __init__(self, Id, rangemin=0, rangemax=1):
        self.Id = Id
        self.rangemin = rangemin
        self.rangemax = rangemax
    def is_binary(self):
        return (self.rangemin==0) and (self.rangemax==1)


def create_chromosome_graph(chromosome, id_generator, genome_name):
    """Creates the vertices and telomeres as well as adjacency and self edges
    of a single Chromosome (chr_kind, [(dir,gene)])
    """
    vertices = []
    edges = []
    #CAUTION: Telomeres need different ids because they cannot be distinguished by h t
    if chromosome[0] == CHR_LINEAR:
        vertices.append(ADJ_Vertex(id_generator.get_new(),
                         EXTREMITY_TELOMERE, TELOMERE_ID,genome_name))
    for orient,gene,tmp_id in chromosome[1]:
        tmp = [ADJ_Vertex(tmp_id,EXTREMITY_TAIL, gene, genome_name)
              ,ADJ_Vertex(tmp_id,EXTREMITY_HEAD, gene, genome_name)]
        if orient==ORIENT_NEGATIVE:
            tmp = tmp[::-1]
        vertices.extend(tmp)
    if chromosome[0] == CHR_LINEAR:
        vertices.append(ADJ_Vertex(id_generator.get_new(),
                     EXTREMITY_TELOMERE, TELOMERE_ID,genome_name))
        old = vertices[0]
        vertices2 = vertices[1::]
    else:
        old = vertices[-1]
        vertices2 = vertices
    #print(map(lambda x: (x.gene_id,x.extremity, x.vertex_id),vertices))
    for new in vertices2:
        edges.append(g_Edge(old,new))
        old = new
    #spurious case that of a singleton circular
    if chromosome[0] == CHR_CIRCULAR and len(chromosome[1]) == 1:
        edges[0].repress_self()
        singleton_circulars.append(edges[1])
    return vertices, edges

def create_genome_graph(genome, id_generator):
    """Creates the vertices and telomeres as well as adjacency and self edges
    for a complete genome (name,[(chr_kind, [(dir,gene)])])
    """
    vertices = []
    edges = []
    for chr in genome[1]:
        v, e = create_chromosome_graph(chr, id_generator, genome[0])
        vertices.extend(v)
        edges.extend(e)
    return vertices, edges

def vertices_by_genes(v_list):
    ''' Generate a dictionary d: (gene_id, extremity) -> [vertices].
    '''
    d = dict()
    for vertex in v_list:
        if (vertex.gene_id,vertex.extremity) not in d:
            d[(vertex.gene_id,vertex.extremity)] = []
        d[(vertex.gene_id,vertex.extremity)].append(vertex)
    return d

def add_to_list_dict(d, key, elem):
	if key in d:
		d[key].append(elem)
	else:
		d[key] = [elem]

def get_cross_genome_edges(v1, v2):
    ''' Generate the matching edges between the vertices v1,v2 of genomes 1 and 2
        in the modified adjacency graph.
    '''
    v1g = vertices_by_genes(v1)
    v2g = vertices_by_genes(v2)
    edges = []
    duplicate_fams = 0
    max_fam = 0
    duplicates = 0
    for gene_id, vertices in v1g.iteritems():
        if gene_id in v2g:
            if len(vertices) > 1 or len(v2g[gene_id]) > 1:
                duplicate_fams+=1
                d = max(len(vertices),len(v2g[gene_id]))
                max_fam = max(max_fam, d)
                duplicates+=d
        edges.extend([g_Edge(u,v) for u in vertices if gene_id in v2g for v in v2g[gene_id]])
    LOG.info('Number of duplicates is: %d\n'%int(duplicates/2))
    LOG.info('Number of duplicate families: %d\n'%int(duplicate_fams/2))
    LOG.info('Greatest family is: %d\n'%max_fam)
    return edges

def create_adjacency_graph(genome1, genome2, id_generator):
    ''' Create the modified adjacency graph including capping and padding from
        two genomes. The id generator is used to generate the
        null extremity ids.
    '''
    #introduce empty telomere-telomere chromosomes
    n_ch1 = len(filter(lambda x: x[0]==CHR_LINEAR, genome1[1]))
    n_ch2 = len(filter(lambda x: x[0]==CHR_LINEAR, genome2[1]))
    #print(genome1, genome2)
    if n_ch1 < n_ch2:
        LOG.debug("Padding genome: %s\n"%genome1[0])
        for i in range(0,n_ch2- n_ch1):
            genome1[1].append((CHR_LINEAR,[]))
    if n_ch2 < n_ch1:
        LOG.debug("Padding genome: %s\n"%genome2[0])
        for i in range(0,n_ch1- n_ch2):
            genome2[1].append((CHR_LINEAR,[]))
    v1, e1 = create_genome_graph(genome1, id_generator)
    v2, e2 = create_genome_graph(genome2, id_generator)
    cross = get_cross_genome_edges(v1,v2)
    v1.extend(v2)
    e1.extend(e2)
    e1.extend(cross)
    #print(filter(lambda x: x.is_telomere()e1))
    return v1, e1

VERTEX_NAME = "%d_%s_%s"
VERTEX_VARIABLE = "%s_%s"
EDGE_VARIABLE = "%s_(%s,%s)"

def vertex_name(v):
    ''' Given a vertex, return its name, that is id_genome_extremity.
    '''
    return VERTEX_NAME%(v.vertex_id, v.genome_id, v.extremity)

def vertex_var_n(v,varname):
    ''' Obtain the string of a vertex variable (baseName_vertexName) in the ILP
        given the vertex and the variable base name.
    '''
    return VERTEX_VARIABLE%(varname,vertex_name(v))

def edge_var_n(e,varname):
    ''' Obtain the string of an edge variable (baseName_(vertex1,vertex2)).
    '''
    return EDGE_VARIABLE%(varname,vertex_name(e.vertex1),vertex_name(e.vertex2))

#not quite clean here
def edge_var_n_tail(e,varname):
    return EDGE_VARIABLE%(varname
                          ,VERTEX_NAME%(e.vertex1.vertex_id,e.vertex1.genome_id,EXTREMITY_TAIL)
                          ,VERTEX_NAME%(e.vertex2.vertex_id,e.vertex2.genome_id,EXTREMITY_TAIL))

def vertex_var(v,varname,rangemin = 0, rangemax = 1):
    ''' Given a vertex and the variable base name, return the correpsonding ILP variable.
    '''
    return ILP_variable(vertex_var_n(v, varname),
     rangemin=rangemin, rangemax=rangemax)

def edge_var(e,varname):
    ''' Given an edge and the variable base name, return the correpsonding ILP variable.
    '''
    return ILP_variable(edge_var_n(e, varname))

DELTA_R = 'delta_r'
def set_variables(ilp, vertices, edges,opt):
    ''' Introduce the existence of all variables to the ILP.
    '''
    for v in vertices:
        ilp.variables.extend([
        vertex_var(v,'z')
        , vertex_var(v,'r')
        , vertex_var(v,'y',0, v.get_i())
        ])
        if not opt:
            ilp.variables.append(vertex_var(v,'d'))
    for e in edges:
        ilp.variables.append(edge_var(e,'x'))
        ilp.variables.append(edge_var(e,DELTA_R))
GEQ = ">="
LEQ = "<="
EQ  = "="
CONST = "C"
def set_run_conditions(ilp, vertices, edges, opt):
    ''' Set the constraints dealing with the run counting variables r, delta_r,
        as well as d if opt=False. Otherwise the "z-reset" is done via y.
    '''
    for e in edges:
        #delta_r_(v,u) >= r_v - r_u -1 - x_(v,u)
        ilp.conditions.append(([(1,edge_var_n(e,DELTA_R))],GEQ,
                               [(1,vertex_var_n(e.vertex1,'r'))
                               ,(-1,vertex_var_n(e.vertex2,'r'))
                               ,(-1,CONST)
                               ,(1,edge_var_n(e,'x'))]))
        #delta_r_(v,u) >= r_u - r_v -1 + x_(v,u)
        ilp.conditions.append(([(1,edge_var_n(e,DELTA_R))],GEQ,
                               [(1,vertex_var_n(e.vertex2,'r'))
                               ,(-1,vertex_var_n(e.vertex1,'r'))
                               ,(-1,CONST)
                               ,(1,edge_var_n(e,'x'))]))
        if not opt:
            #d_v >= d_u + x_(u,v) -1
            ilp.conditions.append(([(1,vertex_var_n(e.vertex1,'d'))],GEQ,
                                  [(1,vertex_var_n(e.vertex2,'d'))
                                  ,(1,edge_var_n(e,'x'))
                                  ,(-1,CONST)]))
            #d_u >= d_v + x_(u,v) -1
            ilp.conditions.append(([(1,vertex_var_n(e.vertex2,'d'))],GEQ,
                                  [(1,vertex_var_n(e.vertex1,'d'))
                                  ,(1,edge_var_n(e,'x'))
                                  ,(-1,CONST)]))
        if e.is_self():
            if not opt:
                #d_u >= x_(u,v)
                ilp.conditions.append(([(1,vertex_var_n(e.vertex1,'d'))],GEQ,[(1,edge_var_n(e,'x'))]))
                ilp.conditions.append(([(1,vertex_var_n(e.vertex2,'d'))],GEQ,[(1,edge_var_n(e,'x'))]))
            if opt:
                #i-i*x_(v_i,u_j) >= y_i
                ilp.conditions.append(([(e.vertex1.get_i(),CONST),(-1*e.vertex1.get_i(),edge_var_n(e,'x'))],GEQ,[(1,vertex_var_n(e.vertex1, 'y'))]))
                #j-j*x_(v_i,u_j) >= y_j
                ilp.conditions.append(([(e.vertex2.get_i(),CONST),(-1*e.vertex2.get_i(),edge_var_n(e,'x'))],GEQ,[(1,vertex_var_n(e.vertex2, 'y'))]))
            if e.vertex1.genome_id==genome1:
                #1 - x_(u,v) >= r_u
                ilp.conditions.append(([(1,CONST),(-1,edge_var_n(e,'x'))],GEQ,[(1,vertex_var_n(e.vertex1,'r'))]))
                #1 - x_(u,v) >= r_v
                ilp.conditions.append(([(1,CONST),(-1,edge_var_n(e,'x'))],GEQ,[(1,vertex_var_n(e.vertex2,'r'))]))
            if e.vertex1.genome_id==genome2:
                #x_(u,v) <= r_u
                ilp.conditions.append(([(1,edge_var_n(e,'x'))],LEQ,[(1,vertex_var_n(e.vertex1,'r'))]))
                #x_(u,v) <= r_v
                ilp.conditions.append(([(1,edge_var_n(e,'x'))],LEQ,[(1,vertex_var_n(e.vertex2,'r'))]))
    if not opt:
        for v in vertices:
            leftside = [(0,CONST)]
            #0 >= z_v + d_v -1
            ilp.conditions.append((leftside,GEQ,
                                   [(1,vertex_var_n(v,'z'))
                                   ,(-1,CONST)
                                   ,(1,vertex_var_n(v,'d'))]))

def edges_by_vertices(e_list):
	''' Generate a dict d: vertex -> [edges]
	'''
	d = dict()
	for e in e_list:
		add_to_list_dict(d,e.vertex1,e)
		add_to_list_dict(d,e.vertex2,e)
	return d

def restrict_runs(edges):
	'''Add the special condition, that run labels cannot change in clean adjacency edges.
	'''
	conditions = []
	#for e in edges:
		# DELTA_R_e <= x_e
	#	conditions.append(([(1,edge_var_n(e,DELTA_R))],LEQ,[(1,edge_var_n(e,'x'))]))
	d = edges_by_vertices(filter(lambda e: e.is_self(), edges))
	for a in filter(lambda e: e.is_adjacency(), edges):
		if a.vertex1.extremity == EXTREMITY_TELOMERE or a.vertex2.extremity == EXTREMITY_TELOMERE:
			continue
		left =  (1,edge_var_n(d[a.vertex1][0], 'x')) # unsafe, but all genes should have a self edge
		right = (1,edge_var_n(d[a.vertex2][0], 'x'))
		conditions.append(([left,right, (-1, edge_var_n(a,DELTA_R))], GEQ, [(0,CONST)]))
		#no label changes between two indels (don't know if optimizes)
		conditions.append(([left,right, (1, edge_var_n(a,DELTA_R))], LEQ, [(2,CONST)]))
	return conditions

def add_vertex_consistency(ilp,vertices,edges):
    ''' Assure that in every feasible solution, each vertex has degree 2.
    '''
    vertex_summands = dict()
    for e in edges:
        v1 = (e.vertex1.vertex_id,e.vertex1.extremity)
        v2 = (e.vertex2.vertex_id,e.vertex2.extremity)
        if v1 not in vertex_summands:
            vertex_summands[v1] = []
        if v2 not in vertex_summands:
            vertex_summands[v2] = []
        vertex_summands[v1].append((1,edge_var_n(e,'x')))
        vertex_summands[v2].append((1,edge_var_n(e,'x')))
    for v in vertices:
        ilp.conditions.append((vertex_summands[(v.vertex_id,v.extremity)],EQ,[(2,CONST)]))

def set_decomp_conditions(ilp,vertices,edges):
    ''' Apply the conditions for a consistent decomposition, i.e. every marker
        matched once, adjacency edges always active etc.
    '''
    add_vertex_consistency(ilp,vertices,edges)
    for e in edges:
        i = e.vertex1
        j = e.vertex2
        #y_i <= y_j + i -i*x_e
        ilp.conditions.append(([(1,vertex_var_n(i,'y'))],LEQ,
                               [(1,vertex_var_n(j,'y'))
                               ,(i.get_i(),CONST)
                               ,(-i.get_i(),edge_var_n(e,'x'))]))
        #y_j <= y_i + j - j*x_e
        ilp.conditions.append(([(1,vertex_var_n(j,'y'))],LEQ,
                               [(1,vertex_var_n(i,'y'))
                               ,(j.get_i(),CONST)
                               ,(-j.get_i(),edge_var_n(e,'x'))]))
        if e.is_adjacency():
            # x_e = 1
            ilp.conditions.append(([(1,edge_var_n(e,'x'))],EQ,[(1,CONST)]))
        if e.is_cross_genome() and e.vertex1.extremity == EXTREMITY_HEAD:
            # x_(u_h,v_h) = x_(u_t, v_t)
            ilp.conditions.append(([(1,edge_var_n(e,'x'))],EQ,[(1,edge_var_n_tail(e,'x'))]))
    for v in vertices:
        # i*z_i <= y_i
        ilp.conditions.append(([(v.get_i(),vertex_var_n(v,'z'))],LEQ,
                               [(1,vertex_var_n(v,'y'))]))

def set_maximization_function(ilp, vertices, edges, opt):
    for v in vertices:
        ilp.maximization_function.append((2,vertex_var_n(v,'z')))
    for e in edges:
        ilp.maximization_function.append((-1,edge_var_n(e,DELTA_R)))


def set_mm_optimizations(ilp,vertices,edges):
    ''' Apply all optimizations following from applying the MM model to the ILP.
    '''
    a = vertices_by_genes(filter(lambda x: x.genome_id==genome1, vertices))
    b = vertices_by_genes(filter(lambda x: x.genome_id==genome2, vertices))
    occ = lambda d, x: 0 if not x in d else len(d[x])
    this = lambda x: a if x == genome1 else b
    other = lambda x: a if x == genome2 else b
    genes =set()
    genes.update(a.keys())
    genes.update(b.keys())
    genes.discard(TELOMERE_ID)
    for g in genes:
        if occ(a,g) ==1 and occ(b,g) ==1:
            v1 = a[g][0]
            v2 = b[g][0]
            e = g_Edge(v1,v2)
            # x_e = 1
            ilp.conditions.append(([(1,edge_var_n(e,'x'))],EQ,[(1,CONST)]))
            ilp.conditions.append(([(1,vertex_var_n(v1,'y'))],EQ,[(1,vertex_var_n(v2,'y'))]))
    for e in filter(lambda x: x.is_self(), edges):
        g = (e.vertex1.gene_id, e.vertex1.extremity)
        genome = e.vertex1.genome_id
        if occ(this(genome),g) <= occ(other(genome),g):
            ilp.conditions.append(([(1,(edge_var_n(e,'x')))],EQ,[(0,CONST)]))
        if occ(other(genome),g) == 0:
            ilp.conditions.append(([(1, edge_var_n(e,'x'))],EQ,[(1,CONST)]))
            #this condition works for all except circular singletons
            if not e in singleton_circulars:
                ilp.conditions.append(([(1, vertex_var_n(e.vertex1,'z'))],EQ,[(0,CONST)]))
                ilp.conditions.append(([(1, vertex_var_n(e.vertex2,'z'))],EQ,[(0,CONST)]))

def preset_delta_r(ilp,edges):
    '''Only allow lable changes along adjacency edges.
    '''
    
    for e in filter(lambda x: x.is_self() or x.is_cross_genome() or x.vertex1.genome_id == genome1, edges):
        ilp.conditions.append(([(1,edge_var_n(e, DELTA_R))], EQ, [(0,CONST)]))
    ilp.conditions.extend(restrict_runs(edges))


def create_ILP(vertices, edges, mm=False, optimize=False):
    ''' Generate the ILP from given vertices and edges of the modified adjacency graph.
    '''
    ilp = ILP()
    set_maximization_function(ilp, vertices, edges, optimize)
    set_variables(ilp, vertices, edges, optimize)
    set_decomp_conditions(ilp, vertices,edges)
    set_run_conditions(ilp,vertices,edges, optimize)
    if mm:
        set_mm_optimizations(ilp,vertices,edges)
    if optimize:
        preset_delta_r(ilp,edges)
    return ilp


EDGE_OUTPUT = "%s_%s -> %s_%s (%s) (%s,%s)\n"
def print_graph(vertices,edges):
    '''Print the generated adjacency graph to debug out.
    '''
    LOG.debug("Adjacency Graph:\n")
    for e in edges:
        g1 = e.vertex1.gene_id
        e1 = e.vertex1.extremity
        g2 = e.vertex2.gene_id
        e2 = e.vertex2.extremity
        id1 = e.vertex1.vertex_id
        id2 = e.vertex2.vertex_id
        kind = "cross"
        if (e.is_adjacency()):
            kind = "adj"
        if (e.is_self()):
            kind="self"
        LOG.debug(EDGE_OUTPUT%(g1,e1,g2,e2,kind,id1,id2))

def smd(kx):
    ''' Turn a summand of form (n, x_i), where n is a constant and x_i a variable
        into a corresponding string nx_i while catching the edge cases n==1 or x_i
        being the identifier for a constant.
    '''
    k = abs(kx[0])
    x = kx[1]
    kk="%d"%k
    if k == 1:
        kk=""
    if x == CONST:
        x=""
        kk="%d"%k
    return "%s %s"%(kk,x)

def sum_str(ls):
    ''' Express a list of constant, variable pairs (n,x_i) as the string of a
        sum of these.
    '''
    r = ""
    if ls[0][0] < 0 :
        r+="- "
    r+=smd(ls[0])
    del ls[0]
    for kx in ls:
        if kx[0] > 0:
            r+=" + "
        else:
            r+=" - "
        r+=smd(kx)
    return r

def normalize_equation(left,sign, right):
    ''' Rewrite a given equation, such that the constant is on the right
        and all variables are to the left.
    '''
    right_ = filter(lambda x: x[1]==CONST,right)
    right_.extend([(-k,x) for (k, x) in left if x==CONST])
    if len(right_) == 0:
        right_.append((0,CONST))
    right_ = reduce(lambda x, y: (x[0]+y[0],CONST),right_)
    right_ = [right_]
    left_ = filter(lambda x: x[1] != CONST, left)
    left_.extend([(-k,x) for (k,x) in right if x != CONST])
    return left_,sign,right_


def print_ILP_cpl(ilp, handle):
    ''' Writes a given ILP to the handle in CPLEX lp format
    (http://lpsolve.sourceforge.net/5.0/CPLEX-format.htm).
    '''
    handle.write("Maximize\n")
    handle.write(" obj: ")
    handle.write(sum_str(ilp.maximization_function))
    handle.write("\n")
    gen = Simple_Id_Generator()
    handle.write("Subject To\n")
    #print(max([len(x) for x in ilp.conditions]))
    for s1, e, s2 in ilp.conditions:
        s1_,e_,s2_ = normalize_equation(s1,e,s2)
        handle.write(" c%d: "%gen.get_new())
        handle.write(sum_str(s1_))
        handle.write(" %s "%e_)
        handle.write(sum_str(s2_))
        handle.write("\n")
    handle.write("Bounds\n")
    for x in filter(lambda x: not x.is_binary(), ilp.variables):
        handle.write(" ")
        handle.write("%d <= %s <= %d\n"%(x.rangemin,x.Id, x.rangemax))
    handle.write("Binary\n")
    for x in filter(lambda x: x.is_binary(), ilp.variables):
        handle.write(" ")
        handle.write(x.Id)
        handle.write("\n")
    handle.write("General\n")
    for x in filter(lambda x: not x.is_binary(), ilp.variables):
        handle.write(" ")
        handle.write(x.Id)
        handle.write("\n")
    handle.write("End\n")

def id_genomes(genomes, gen):
    ''' Assign unique identifiers to the genes via the provided generator.
    '''
    return map(lambda x: id_genome(x,gen), genomes)

def id_genome(genome,gen):
    (name, chromosomes) = genome
    return (name, map(lambda x: id_chr(x,gen), chromosomes))

def id_chr(chr, gen):
    (orient, list) = chr
    return (orient, map(lambda x: id_gene(x,gen), list))

def id_gene(gene, gen):
    (orient,name) = gene
    return (orient, name, gen.get_new())

def singleton_constraints(genomes, ilp, edges):
    gen = Simple_Id_Generator()
    d = dict([(e.vertex1.vertex_id, e) for e in edges if e.is_self()])
    for gnm in genomes:
        for chrm in [x[1] for x in gnm[1] if x[0]==CHR_CIRCULAR]:
            cid = gen.get_new()
            s = 's_%d'%cid
            ilp.variables.append(ILP_variable(s,0,1))
            smm = []
            sz = len(chrm)
            for o, g, gid in chrm:
                e = d[gid]
                smm.append((1,edge_var_n(e,'x')))
            smm.append((-sz+1,CONST))
            ilp.conditions.append(([(1,s)],GEQ,smm))
            ilp.maximization_function.append((-2,s))
    return ilp

def main():
    epilog = "This script assumes the Unimog file has exactly two genomes. For selecting two genomes in an unimog file containing multiple ones (with unique names), both options -1/--genome1 and -2/--genome2 must be used."
    
    parser = ArgumentParser(description='Read and id an unimog file with two genomes and compute the corresponding DING ILP.', epilog=epilog)
    parser.add_argument('-i', nargs=1, required=True, help='Input File with exactly two genomes (labeled "A","B") in Unimog format.')
    parser.add_argument('-u', nargs=1, required=True, help='Output File for uniquely labelled occurrences in Unimog format.')
    parser.add_argument('-o', nargs=1, required=True, help='Output File for the resulting ILP in CPLEX lp format.')
    parser.add_argument('-1', '--genome1', dest='genome1', metavar='A', type=str, required=False,
                        help='Name of the first genome you want to compare (must be one of the genomes in the Unimog file).')
    parser.add_argument('-2', '--genome2', dest='genome2', metavar='B', type=str, required=False,
                        help='Name of the second genome you want to compare (must be one of the genomes in the Unimog file).')
    parser.add_argument('--opt', nargs=1, choices=('s','mm','all','none'), help=argparse.SUPPRESS, default=['all'] )
    parser.add_argument('-l',nargs=1, help='Log-file')
    parser.add_argument('-v', action="store_true", help="Be verbose.")
    parser.add_argument('--ignore-circular-singletons', action="store_true", help="Use only if ABSOLUTELY certain, that the matching solution will not contain circular singletons. Else distances and matchings computed using this option could be corrupted.")
    args = parser.parse_args()

    if (not args.genome1 and args.genome2) or (args.genome1 and not args.genome2):
        raise Exception, "Please provide both both options -1/--genome1 and -2/--genome2 or none of them!"

    st = logging.StreamHandler(sys.stderr)
    if args.l:
        st = logging.FileHandler(args.l[0])
    st.setLevel(logging.DEBUG)
    st.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s'))
    ch = logging.StreamHandler(sys.stdout)
    if args.v:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s'))
    LOG.addHandler(ch)
    LOG.addHandler(st)
    LOG.info("Starting %s generating the DING ILP from %s."%(sys.argv[0],args.i[0]))
    if args.opt != ['all']:
        LOG.warning("'--opt' is a deprecated parameter and to be used for testing purposes only. Anything other than 'mm' or 'all' will not apply the Maximum Matching model.")
    with open(args.i[0]) as file:
        data = file.readlines()

    if args.genome1:
        genomes = readGenomes(data, genomesOnly=(args.genome1, args.genome2))
        if args.genome1 != genomes[0][0]: genomes.reverse()
    else:
        genomes = readGenomes(data)
    
    if len(genomes) !=2:
        raise Exception, "Please provide exactly two genomes in the Unimog file or use the options -1/--genome1 and -2/--genome2!"
    genomes[0] = (genome1, genomes[0][1])
    genomes[1] = (genome2, genomes[1][1])
    gen = Simple_Id_Generator()
    genomes = id_genomes(genomes, gen)
    LOG.info("Writing uniquely labeled genes to file %s."%args.u[0])
    with open(args.u[0], "w") as out:
        print_id_genome_unimog(genomes[0],out)
        print_id_genome_unimog(genomes[1],out)
    LOG.info("Creating adjacency graph.")
    v, e = create_adjacency_graph(genomes[0],genomes[1], gen)
    print_graph(v,e)
    opt = False
    mm = False
    if 's' in args.opt or 'all' in args.opt:
        opt = True
    if 'mm' in args.opt or 'all' in args.opt:
        mm =True
    LOG.info("Generating DING ILP.")
    ilp = create_ILP(v, e, mm, opt)
    if args.ignore_circular_singletons:
        LOG.warning("Circular singletons will not be handeled. If any exist, the solution will be corrupted. There will be no further warning on this issue.")
    else:
        ilp = singleton_constraints(genomes, ilp, e)
    LOG.info("Writing ILP.")
    with open(args.o[0], "w") as outfile:
        print_ILP_cpl(ilp, outfile)
    LOG.info("DONE. Exiting.")

main()
