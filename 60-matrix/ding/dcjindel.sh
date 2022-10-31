#!/usr/bin/bash

function extract_organism_name_from_path {
    echo ${1} | rev | cut -d '/' -f 1 | rev | cut -d . -f 1
}

GENOME_A=$(extract_organism_name_from_path $1)
GENOME_B=$(extract_organism_name_from_path $2)
UNIMOG_FILE_NAME="${GENOME_A}-vs-${GENOME_B}"
PARENT_PATH=$(cd $(dirname "${BASH_SOURCE[0]}"); pwd -P)

${PARENT_PATH}/genome2unimog.py --input $1 $2 --output ${PARENT_PATH}/${UNIMOG_FILE_NAME}.unimog

${PARENT_PATH}/unimog_to_ilp.py -i ${UNIMOG_FILE_NAME}.unimog -u ${UNIMOG_FILE_NAME}.ids -o ${UNIMOG_FILE_NAME}.lp 2> /dev/null

gurobi_cl ResultFile=${UNIMOG_FILE_NAME}.sol ${UNIMOG_FILE_NAME}.lp > /dev/null

DISTANCE=$(${PARENT_PATH}/parse_gurobi_sol.py \
    -i ${UNIMOG_FILE_NAME}.sol \
    -u ${UNIMOG_FILE_NAME}.ids \
    -o ${UNIMOG_FILE_NAME}_relabeled.unimog | cut -f 3 | tail -n 1)

echo -e "${GENOME_A}\t${GENOME_B}\t${DISTANCE}"
