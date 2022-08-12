#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""extr.py
   Genome Extremity module
   exports class Extremity offering the following methods:
   - constructor(name, charge):
   constructs new extremity with given data
   - charge(): 
   returns an integer, the charge of the extremity; charge is to be
   used as follows: +1 if in g1 only, -1 if in g2 only, 0 if in both.
   Also exports
   - find(name, charge):
   returns an extremity with the name 'name' and 'charge';  if name
   already exists, adds to the charge and returns existing.

"""
extr = {}

class Extremity:
    def __init__(self, name, charge):
        self.name = name
        self.charge = charge

    def charge(self):
        return self.charge

    def __str__(self):
        return '{0}({1})'.format(self.name, self.charge)

def find(name, charge):
    if name in extr:
        e = extr[name]
        e.charge += charge
    else:
        e = Extremity(name, charge)
        extr[name] = e
    return e
