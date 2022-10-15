DATA := ../60-matrix
SAMPLES := ../45-jackknife/samples
NSAMPLES := $(shell ls ${SAMPLES} | wc -l)
OUTGROUP := ""

.PHONY: rankc_nj_rooted_tree rank_nj_rooted_tree rankindl_nj_rooted_tree dcj_nj_rooted_tree clean

rankc_nj_rooted_tree: ${DATA}
	for i in `seq 1 ${NSAMPLES}`; do \
	    ./rooted-nj-tree-with-outgroup.R $</rankc_matrix_$${i}.mat rankc_nj_tree_$${i} ${OUTGROUP}; \
	done

rankindl_nj_rooted_tree: ${DATA}
	for i in `seq 1 ${NSAMPLES}`; do \
	    ./rooted-nj-tree-with-outgroup.R $</rankindl_matrix_$${i}.mat rankindl_nj_tree_$${i} ${OUTGROUP}; \
	done

rank_nj_rooted_tree: ${DATA}
	for i in `seq 1 ${NSAMPLES}`; do \
	    ./rooted-nj-tree-with-outgroup.R $</rank_matrix_$${i}.mat rank_nj_tree_$${i} ${OUTGROUP}; \
	done

dcj_nj_rooted_tree: ${DATA}
	for i in `seq 1 ${NSAMPLES}`; do \
	    ./rooted-nj-tree-with-outgroup.R $</dcj_matrix_$${i}.mat dcj_nj_tree_$${i} ${OUTGROUP}; \
	done

clean:
	rm -f *.png *.nwk
