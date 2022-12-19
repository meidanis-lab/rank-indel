#!/usr/bin/bash

if [[ -z $1 ]]
then
    echo "usage: $0 [rank | rankindl | rankc | dcj]"
    exit 0
elif [[ $1 == "dcj" ]]
then
    DIST="dcj"
elif [[ $(expr substr $1 1 4) == "rank" ]]
then
    DIST="rank"
fi

for i in $(seq 0.0 0.1 0.9)
do
    for j in $(seq 10)
    do
        make -B $1 INSRATE=${i} DELRATE=${i};
        mv ${DIST}/$1_tree.nwk ${DIST}/$1_tree_indel-${i}_iter${j}.nwk;
        mv ${DIST}/$1_tree_indel-${i}_iter${j}.nwk ${DIST}/results_for_indel-rate
    done
done
