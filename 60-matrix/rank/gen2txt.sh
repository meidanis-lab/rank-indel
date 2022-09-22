#!/usr/bin/bash

# If the first char is '(', then the chromosome is circular;
# in this case, the 1st extremity is adjacent to the last extremity.
# Print the extremities in between.
# Notice that we start at 3 to skip the enclosing braces or brackets, and
# the 1st extremity.
# In the case of linear genomes, the telomeres are ignored.
cat $1 |
    awk '{
        if ($1=="(") 
            print $2 " " $(NF-1);
        for (i=3; i<NF-1; i=i+2)
            print $i " " $(i+1)
    }'
