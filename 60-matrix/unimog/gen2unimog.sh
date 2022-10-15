#!/usr/bin/bash

function extract_organism_strain {
    echo ${1} | rev | cut -d '/' -f 1 | rev | cut -d . -f 1 | cut -d '_' -f 3-
}

GENOME_NAME="T_$(extract_organism_strain $1)"

# put header
echo ">${GENOME_NAME}"
# put chromosomes
cat $1 | awk '{$1=""; print substr($0,2)}'
