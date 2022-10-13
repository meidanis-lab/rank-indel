#!/usr/bin/env python

## efficient rank computation

def iter_distance(A, B, n):
    visited = set()
    rank = n
    ncycles = 0
    abnulls = 0

    for i in A:
        if i not in visited:
            rank -= _iter_distance(A, B, i, visited)

    return rank

def _iter_distance(A, B, i, visited):
    visited.add(i)
    stack = [i]

    while stack:
        j = stack.pop()
        if j not in visited:
            if False:  # need to handle AB-null paths
                pass
            elif B[A[j]] in visited:
                return 1
            elif B[A[j]] != 0:
                visited.append(B[A[j]])

def distance(A, B, n):
    visited = set()
    rank = n
    ncycles = 0
    nabnulls = 0

    ## 1st pass: look for AB-null paths
    for i in A:
        if i not in visited:
            if A[i] == 0 and B[i] == 0:
                visited.add(i)
                rank -= 1
                nabnulls += 1
            elif B[i] == 0:
                res = search(A, B, i, visited)
                rank -= res
                nabnulls += res
    
    ## 2nd pass: "eliminate" A-null paths from search
    for i in A:
        if i not in visited and A[i] == 0:
            visited.add(i)

    ## 3rd pass: look for cycles
    for i in A:
        if i not in visited and A[i] != 0 and B[i] != 0:
            res = search(A, B, i, visited)
            rank -= res
            ncycles += res
    return rank, ncycles, nabnulls

def search(A, B, i, visited):
    visited.add(i)
    if A[i] == 0:
        return 1
    elif B[A[i]] in visited:
        return 1
    elif B[A[i]] != 0:
        return search(A, B, B[A[i]], visited)
    else:
        return 0

## auxiliary functions

def adjs2dict(adjs):
    genome = dict()
    for extr1, extr2 in adjs:
        genome[extr1] = extr2
        genome[extr2] = extr1
    return genome

def add_null_extrs(genome1, genome2):
    for extr in genome1:
        if extr not in genome2:
            genome2[extr] = 0
    for extr in genome2:
        if extr not in genome1:
            genome1[extr] = 0

if __name__ == '__main__':
    # Fix the following ordering
    # 1 = at; 2 = ah; 3 = bt; 4 = bh; 5 = ct; 6 = ch; 7 = dt; 8 = dh.
    #
    # A
    # 1 2 3 4 5 6 7 8
    # 1 3 2 6 5 4 0 0
    #
    # B
    # 1 2 3 4 5 6 7 8
    # 1 4 7 2 0 0 3 8
    #
    # >>> A = [0, 2, 1, 5, 4, 3, -1, -1]
    # >>> B = [0, 3, 6, 1, -1, -1, 2, 7]
    # >>> print(distance(A, A, len(A)))
    # 0
    # >>> print(distance(A, B, len(A)))
    # 6

    import sys

    with open(sys.argv[1], 'r') as adjs_A, open(sys.argv[2], 'r') as adjs_B:
        A = adjs2dict([tuple(line.strip().split()) for line in adjs_A])
        B = adjs2dict([tuple(line.strip().split()) for line in adjs_B])

    add_null_extrs(A, B)

    rank, ncycles, nabnulls = distance(A, B, len(A))

    format_output = lambda s: s.split('/')[-1].split('.')[0]
    print(f'{format_output(sys.argv[1])}\t{format_output(sys.argv[2])}\t{rank}')

    if len(sys.argv) > 3 and sys.argv[3] == '-v':
        print(f'c {ncycles}\tpAB {nabnulls}')

