# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# auxiliary scripts
RANK := ../../60-matrix/rank/dist_rank.sh
RANKC := ../../60-matrix/rank/rank.py
RANKINDL := ../../60-matrix/rank/dist_rankindl.sh
BUILD_MATRIX := ../../60-matrix/build_distance_matrix.py
GEN_COMPS := ../../60-matrix/gen_pairwise_comparisons.py
ROOTED_TREE := ../../70-tree/rooted-nj-tree-with-outgroup.R

.PHONY: split_unimog unimog2pairs unimog2adj clean

%_tree: %_matrix.mat
	${ROOTED_TREE} $< $@ ${OUTGROUP}

rank: ${RANK} unimog2adj
rankc: ${RANKC} unimog2adj
rankindl: ${RANKINDL} unimog2adj
rank rankc rankindl:
	ls L*.txt | xargs ${GEN_COMPS} | parallel --colsep '\t' $< {} | tr '\t' ',' | ${BUILD_MATRIX} - > $@_matrix.mat

unimog2adj: split_unimog
	for i in L*; do \
	    ./unimog2adj.py $${i} > $${i}.adj; \
	    rm $${i} && mv $${i}.adj $${i}; \
	done

split_unimog: ../dummy_data.unimog
	./split_unimog.sh $<

clean:
	rm -f *.txt *.nwk *.csv *.mat
