#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""comp.py
   Implements components for disjoint-set collection.
"""
import extr

class Component:
    """Implementation of components (or, more generally, nodes) for
       our particular disjoint-set collection on bpgraph components.
       Offers methods:
       - constructor: from an Extremity
       - size(): returns size of component (integer), i.e., # of
       extremities in it
       - cycle(): boolean (true iff it's a cycle)
       - term1(): one of the terminals, if not cycle; None if cycle
       - term2(): the other terminal, if not cycle; None if cycle
       - equality test, as any class

       Implementation details:
       Each node has has:
       term1, term2: (only valid for component, i.e., root nodes) its
       terminals when not a cycle; None if cycle
       parent: its parent node
       rank: to implement union-find (not related to rank distance)
       count: number of elements in component; only valid if root node.
    """
    def __init__(self, extr):
        self.term1 = extr
        self.term2 = extr
        self.parent = self
        self.rank = 0
        self.count = 1

    def size(self):
        return self.count

    def cycle(self):
        return self.term1 is None

    def term1():
        return self.term1

    def term2():
        return self.term2

    def __str__(self):
        res = 'term1: {0} term2: {1} rank: {2} count: {3}'
        return res.format(self.term1.__str__(), self.term2.__str__(), self.rank, self.count)

class DSCollection:
    """Implementation our particular disjoint-set collection on
       bpgraph components.
       Offers methods:
       - construtor: inicializes an empty collection
       - add(Extremity): adds new singleton to the collection
       - find(Extremity): returns the component of a given Extremity
       - union(s1, s2, charge): unites components of strings e1 and e2, if
         distinct; closes component if the same; creates extremities
         and components as needed, with charge or adding charge.
       - close(c1): transforms an acyclic component into a cycle
       - iteration over components
    """
    def __init__(self):
        self.comp = set()
        self.node = {}
        self.cycles = 0

    def add(self, extr):
        c = Component(extr)
        self.node[extr] = c
        self.comp.add(c)

    def find(self, s, charge):
        ## if string does not exist yet, create; in any case, add charge
        e = extr.find(s, charge)
        if e not in self.node:
            self.add(e)
        c = self.node[e]
        while c.parent != c:
            c = c.parent
        return (e, c)

    def union(self, s1, s2):
        (e1, c1) = self.find(s1, 0)
        (e2, c2) = self.find(s2, 0)
        ## should check whether s1 and s2 are the two terminals
        if c1 == c2:
            ## close cycle
            c1.term1 = None
            c1.term2 = None
            self.cycles += 1
        else:
            merged = c1 if c1.rank >= c2.rank else c2
            t1 = c1.term2 if c1.term1 == e1 else c1.term1
            t2 = c2.term2 if c2.term1 == e2 else c2.term1
            merged.term1 = t1
            merged.term2 = t2
            if merged == c1:
                c2.parent = c1
                self.comp.remove(c2)
            else:
                c1.parent = c2
                self.comp.remove(c1)
            if c1.rank == c2.rank:
                merged.rank = c1.rank + 1
            else:
                merged.rank = max(c1.rank, c2.rank)
            merged.count = c1.count + c2.count

    def __str__(self):
        res = 'comps: '
        for s in self.comp:
            res += s.__str__() + ' '
        res += 'nodes: '
        for n in self.node:
            res += n.__str__() + ':' + self.node[n].__str__() + ' '
        return res
