# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# result dir
OUTPUT_DIR := results

# auxiliary scripts
DCJ := ../60-matrix/dcj
RANK := ../60-matrix/rank/dist.py 0 0
RANKINDL := ../60-matrix/rank/dist.py 0 1
MAKE_MATRIX := ../60-matrix/build_distance_matrix.py
GEN_COMPS := ../60-matrix/gen_pairwise_comparisons.py
# this one is run from OUTPUT_DIR folder
ROOTED_TREE := ../../70-tree/rooted-nj-tree-with-outgroup.R

# simulator parameters
INSERTION_RATE := 0.2
DELETION_RATE := 0.4
NGENES := 5000
NCHRS := 2
INDEL_SIZE := 4

.PHONY: split_unimog unimog2adj clean

%_tree: %_matrix_${NGENES}.csv
	cd ${OUTPUT_DIR} && ${ROOTED_TREE} $< $@ ${OUTGROUP}

rank_matrix_${NGENES}.csv: unimog2adj
	ls L*.txt | xargs ${GEN_COMPS} | parallel --colsep '\t' ${RANK} {} | tr '\t' ',' | ${MAKE_MATRIX} - > ${OUTPUT_DIR}/$@

rankindl_matrix_${NGENES}.csv: unimog2adj
	ls L*.txt | xargs ${GEN_COMPS} | parallel --colsep '\t' ${RANKINDL} {} | tr '\t' ',' | ${MAKE_MATRIX} - > ${OUTPUT_DIR}/$@

dcj_matrix_${NGENES}.csv: unimog2pairs
	ls *_vs_*.unimog | parallel --colsep '\t' ./dcjindel.sh {} | tr '\t' ',' | ./build_distance_matrix.py - > $@

unimog2pairs: dummy_data_${NGENES}.unimog
	./unimog2pairs.py $<

unimog2adj: split_unimog
	for i in L*; do \
	    ./unimog2adj.py $${i} > $${i}.adj; \
	    rm $${i} && mv $${i}.adj $${i}; \
	done

split_unimog: dummy_data_${NGENES}.unimog
	./split_unimog.sh $<

dummy_data_${NGENES}.unimog: dummy_tree.nwk
	./simulate_dcj.py \
	    -g ${NGENES} \
	    -x ${NCHRS} \
	    -i ${INSERTION_RATE} \
	    -e ${DELETION_RATE} \
	    --indel_size_zipf ${INDEL_SIZE} \
	    -c -l $< 2> simulate_dcj.log > $@

dummy_tree.nwk:
	ngesh -L 20 -x enum -r seed > $@

clean:
	rm -f results/* *.png *.txt *.nwk *.gen *.unimog *.lp *.sol *.ids *.log *.csv
