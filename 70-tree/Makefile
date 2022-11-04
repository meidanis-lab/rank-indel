DATA := ../60-matrix
SAMPLES := ../45-jackknife/samples
NSAMPLES := $(shell ls ${SAMPLES} | wc -l)
OUTGRP := ""
DIST := rank
ifeq (${DIST},dcj)
    FMT := phylip
else
    FMT := csv
endif

.PHONY: ${DIST}_nj_rooted_tree clean

${DIST}_nj_rooted_tree: ${DATA}
	for i in `seq 1 ${NSAMPLES}`; do \
	    ./rooted-nj-tree-with-outgroup.R $</${DIST}_matrix_$${i}.mat ${DIST}_nj_tree_$${i} ${OUTGRP} ${FMT}; \
	done

clean:
	rm -f *.png *.nwk
