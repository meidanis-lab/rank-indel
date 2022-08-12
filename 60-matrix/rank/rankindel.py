#!/usr/bin/python3

class Genome:
    def __init__(self):
        self._adjacencies = dict()
        self._extremities = set()
    def __len__(self):
        return len(self._adjacencies)
    def __setitem__(self, k, v):
        self._adjacencies[k] = v
        self._extremities.add(k)
    def __getitem__(self, k):
        return self._adjacencies[k]
    @property
    def extremities(self):
        return self._extremities
    @property
    def adjacencies(self):
        return self._adjacencies
    def free_end(self, x):
        return self._adjacencies[x] == x
    def null(self, x):
        # A/B-null extremities can be simply non existent in our dictionary
        return x not in self._adjacencies
    def _construct(self, extremities):
        for i, j in zip(extremities[1:-1:2], extremities[2:-1:2]):
            self[i] = j
            self[j] = i
    def add_linear_chr(self, extremities):
        if extremities:
            self[extremities[0]] = extremities[0]
            self[extremities[-1]] = extremities[-1]
            self._construct(extremities)
    def add_circular_chr(self, extremities):
        if extremities:
            self[extremities[0]] = extremities[-1]
            self[extremities[-1]] = extremities[0]
            self._construct(extremities)

def distance(A, B):
    not_visited = A.extremities.union(B.extremities)
    distance = len(not_visited)

    while not_visited:
        value = 0
        to_visit = [not_visited.pop()]
        cycle = False
        while to_visit:
            i = to_visit.pop()

            if (not A.null(i) and not B.null(i) and
                not A.free_end(i) and not B.free_end(i) and
                # A[i] and B[i] were visited, i.e. adjacency was already visited
                (A[i] not in not_visited) and (B[i] not in not_visited)):
                cycle = True

            if not A.null(i):
                value += 1
                if A[i] in not_visited:
                    not_visited.remove(A[i])
                    to_visit.append(A[i])

            if not B.null(i):
                value -= 1
                if B[i] in not_visited:
                    not_visited.remove(B[i])
                    to_visit.append(B[i])

        if value == 0:
            distance -= 1

        # cycle needs to take one extra unit
        if cycle:
            distance -= 1
    return distance

if __name__ == '__main__':
    from argparse import ArgumentParser

    def construct_genome(chr_file):
        genome = Genome()
        for line in chr_file:
            if not line.startswith('(') and not line.startswith('['):
                raise ValueError(f'invalid line in file: {line}')
            chromosome = line.strip()
            if chromosome.startswith('(') and chromosome.endswith(')'):
                genome.add_circular_chr(chromosome[1:-1].split())
            elif chromosome.startswith('[') and chromosome.endswith(']'):
                genome.add_linear_chr(chromosome[1:-1].split())
            else:
                raise ValueError('chromosome in file must be enclosed either in ( ) or [ ]')
        return genome

    DESCRIPTION = 'Compute rank-indel distance between pair of genomes'
    parser = ArgumentParser(DESCRIPTION)
    parser.add_argument('A', help='path for input file of genome A in "adjacencies" format')
    parser.add_argument('B', help='path for input file of genome B in "adjacencies" format')
    args = parser.parse_args()

    with open(args.A, 'r') as file_A, open(args.B, 'r') as file_B:
        genome_A = construct_genome(file_A)
        genome_B = construct_genome(file_B)

    # removes extension from file
    format_genome_id = lambda infile: infile.split('/')[-1].split('.')[0]
    print(f"{format_genome_id(args.A)}\t{format_genome_id(args.B)}\t{distance(genome_A,genome_B)}")
