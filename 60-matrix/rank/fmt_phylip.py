#!/usr/bin/env python

import sys

## for PHYLIP, identifier must have exactly 10 characters
## we adopt the following convention: E_coli_123456789 ==> Ec12345678
## that is, one upper letter for genus, one upper letter for species, and 8 letters for PREFIX of strain
suffix = lambda ident: ident.split('_')[-1][:6]
prefix = lambda ident: ident[0] + ident[2].upper()
get_organism = lambda path: path.split('/')[-1].split('.')[0]
fmt_ident = lambda organism: prefix(organism) + '_' + suffix(organism)

print(fmt_ident(get_organism(sys.argv[1])))
