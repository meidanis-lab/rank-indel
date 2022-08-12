# default number of genes
NGENES := 5000
# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20
# distances
RANK := ../60-matrix/rank-joao/dist.py 0 0
RANKINDL := ../60-matrix/rank-joao/dist.py 0 1
# build matrix
MATRIX := ../60-matrix/build_distance_matrix.py
# result dir
OUTPUT_DIR := results

.PHONY: unimog2gen clean

%_tree: %_matrix_${NGENES}.csv
	../70-tree/rooted-nj-tree-with-outgroup.R $< $@ ${OUTGROUP}

rank_matrix_${NGENES}.csv: unimog2gen
	ls *.gen | xargs ../60-matrix/gen_pairwise_comparisons.py | parallel --colsep '\t' ${RANK} {} | tr '\t' ',' | ../60-matrix/build_distance_matrix.py - > ${OUTPUT_DIR}/$@

rankindl_matrix_${NGENES}.csv: unimog2gen
	ls *.gen | xargs ../60-matrix/gen_pairwise_comparisons.py | parallel --colsep '\t' ${RANKINDL} {} | tr '\t' ',' | ../60-matrix/build_distance_matrix.py - > ${OUTPUT_DIR}/$@

unimog2gen: ${OUTPUT_DIR}/dummy_data_${NGENES}.unimog
	./unimog2gen.sh $<

dummy_data_${NGENES}.unimog: dummy_tree.nwk
	./simulate_dcj.py -g ${NGENES} -x 2 -i 0.2 -e 0.4 --indel_size_zipf 4 -c -l $< 2> simulate_dcj.log > ${OUTPUT_DIR}/$@

dummy_tree.nwk:
	ngesh -L 20 -x enum -r seed > $@

clean:
	rm -f *.nwk *.gen *.unimog *.lp *.sol *.ids *.log *.csv
