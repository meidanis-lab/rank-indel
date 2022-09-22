#!/usr/bin/env python

import fileinput

with fileinput.input() as fin:
    syntenies = fin.readline()
    linear = syntenies.startswith('[')
    circular = syntenies.startswith('(')
    syntenies = syntenies.strip(' []()\n')

result = []
for synteny in syntenies.split():
    tail = synteny + '_t'
    head = synteny + '_h'
    if synteny.startswith('-'):
        result.extend([head[1:], tail[1:]])
    else:
        result.extend([tail, head])

if circular:
    print('( ' + ' '.join(result) + ' )')
elif linear:
    print('[ ' + ' '.join(result) + ' ]')
else:
    raise SystemExit('Not circular nor linear.')
