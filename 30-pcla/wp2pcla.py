#!/usr/bin/env python

import sys
import fileinput

pcla = {}
with fileinput.input(files=sys.argv[1]) as fin:
    for line in fin:
        a = line.split()
        pcla[a[1]] = a[0]

for wp_file in sys.argv[2:]:
    pcla_file = wp_file.replace('wp', 'pcla')
    path_curr_dir = pcla_file.split('/')[-1]
    with open(wp_file, 'r') as infile, open(path_curr_dir, 'w') as outfile:
        for line in infile:
            wp = line[1:15]
            if wp in pcla:
                outfile.write(line[0] + pcla[wp] + '\n')
            else:
                outfile.write(line[0] + wp + '\n')
