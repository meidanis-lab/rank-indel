# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# result dir
OUTPUT_DIR := results

# auxiliary scripts
RANK := ../60-matrix/rank-joao/dist.py 0 0
RANKINDL := ../60-matrix/rank-joao/dist.py 0 1
MAKE_MATRIX := ../60-matrix/build_distance_matrix.py
GEN_COMPS := ../60-matrix/gen_pairwise_comparisons.py
ROOTED_TREE := ../70-tree/rooted-nj-tree-with-outgroup.R

# simulator parameters
INSERTION_RATE := 0.2
DELETION_RATE := 0.4
NGENES := 5000
NCHRS := 1
INDEL_SIZE := 4

.PHONY: unimog2adj clean

%_tree: %_matrix_${NGENES}.csv
	${ROOTED_TREE} $< $@ ${OUTGROUP}

rank_matrix_${NGENES}.csv: unimog2adj
	ls L*.txt | xargs ${GEN_COMPS} | parallel --colsep '\t' ${RANK} {} | tr '\t' ',' | ${MAKE_MATRIX} - > ${OUTPUT_DIR}/$@

rankindl_matrix_${NGENES}.csv: unimog2adj
	ls L*.txt | xargs ${GEN_COMPS} | parallel --colsep '\t' ${RANKINDL} {} | tr '\t' ',' | ${MAKE_MATRIX} - > ${OUTPUT_DIR}/$@

unimog2adj: ${OUTPUT_DIR}/dummy_data_${NGENES}.unimog
	./split_unimog.sh $<
	for i in L*; do \
	    ./unimog2adj.py $${i} > $${i}.adj; \
	    rm $${i} && mv $${i}.adj $${i}; \
	done

dummy_data_${NGENES}.unimog: dummy_tree.nwk
	./simulate_dcj.py \
	    -g ${NGENES} \
	    -x ${NCHRS} \
	    -i ${INSERTION_RATE} \
	    -e ${DELETION_RATE} \
	    --indel_size_zipf ${INDEL_SIZE} \
	    -c -l $< 2> simulate_dcj.log > ${OUTPUT_DIR}/$@

dummy_tree.nwk:
	ngesh -L 20 -x enum -r seed > $@

clean:
	rm -f *.nwk *.gen *.unimog *.lp *.sol *.ids *.log *.csv
