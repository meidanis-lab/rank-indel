#!/usr/bin/bash

DCJ="../../60-matrix/ding"
GENOME_A=$(echo $1 | cut -d. -f1 | cut -d_ -f1)
GENOME_B=$(echo $1 | cut -d. -f1 | cut -d_ -f3)
UNIMOG_FILE_NAME="${GENOME_A}_vs_${GENOME_B}"
PARENT_PATH=$(cd $(dirname "${BASH_SOURCE[0]}"); pwd -P)

${DCJ}/unimog_to_ilp.py -i ${PARENT_PATH}/${UNIMOG_FILE_NAME}.unimog -u ${PARENT_PATH}/${UNIMOG_FILE_NAME}.ids -o ${PARENT_PATH}/${UNIMOG_FILE_NAME}.lp 2> /dev/null
gurobi_cl ResultFile=${UNIMOG_FILE_NAME}.sol ${UNIMOG_FILE_NAME}.lp > /dev/null
DISTANCE=$(${DCJ}/parse_gurobi_sol.py \
	 -i ${PARENT_PATH}/${UNIMOG_FILE_NAME}.sol \
	 -u ${PARENT_PATH}/${UNIMOG_FILE_NAME}.ids \
	 -o ${PARENT_PATH}/${UNIMOG_FILE_NAME}_relabeled.unimog | cut -f 3 | tail -n 1)
echo -e "${GENOME_A}\t${GENOME_B}\t${DISTANCE}"
