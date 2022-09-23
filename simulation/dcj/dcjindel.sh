#!/usr/bin/bash

DCJ="../../60-matrix/dcj"
GENOME_A=$(echo $1 | cut -d. -f1 | cut -d_ -f1)
GENOME_B=$(echo $1 | cut -d. -f1 | cut -d_ -f3)
UNIMOG_FILE_NAME="${GENOME_A}_vs_${GENOME_B}"

${DCJ}/unimog_to_ilp.py -i ${UNIMOG_FILE_NAME}.unimog -u ${UNIMOG_FILE_NAME}.ids -o ${UNIMOG_FILE_NAME}.lp 2> /dev/null
gurobi_cl ResultFile=${UNIMOG_FILE_NAME}.sol ${UNIMOG_FILE_NAME}.lp > /dev/null
DISTANCE=$(${DCJ}/parse_gurobi_sol.py \
	 -i ${UNIMOG_FILE_NAME}.sol \
	 -u ${UNIMOG_FILE_NAME}.ids \
	 -o ${UNIMOG_FILE_NAME}_relabeled.unimog | cut -f 3 | tail -n 1)
echo -e "${GENOME_A}\t${GENOME_B}\t${DISTANCE}"
