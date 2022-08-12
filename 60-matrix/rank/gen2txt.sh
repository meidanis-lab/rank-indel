#!/usr/bin/bash

cat $1 | sed 's/^.\(.*\).$/\1/' | awk '{for (i=1; i<= NF; i=i+2) print $i " " $(i+1)}'
