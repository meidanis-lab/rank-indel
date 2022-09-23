# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# auxiliary scripts
RANK := ../../60-matrix/rank/dist.py 0 0
RANKINDL := ../../60-matrix/rank/dist.py 0 1
BUILD_MATRIX := ../../60-matrix/build_distance_matrix.py
GEN_COMPS := ../../60-matrix/gen_pairwise_comparisons.py
ROOTED_TREE := ../../70-tree/rooted-nj-tree-with-outgroup.R

.PHONY: split_unimog unimog2pairs unimog2adj clean

%_tree: %_matrix.csv
	${ROOTED_TREE} $< $@ ${OUTGROUP}

rank_matrix.csv: unimog2adj
	ls L*.txt | xargs ${GEN_COMPS} | parallel --colsep '\t' ${RANK} {} | tr '\t' ',' | ${BUILD_MATRIX} - > $@

rankindl_matrix.csv: unimog2adj
	ls L*.txt | xargs ${GEN_COMPS} | parallel --colsep '\t' ${RANKINDL} {} | tr '\t' ',' | ${BUILD_MATRIX} - > $@

unimog2adj: split_unimog
	for i in L*; do \
	    ./unimog2adj.py $${i} > $${i}.adj; \
	    rm $${i} && mv $${i}.adj $${i}; \
	done

split_unimog: ../dummy_data.unimog
	./split_unimog.sh $<

clean:
	rm -f *.txt *.nwk *.csv