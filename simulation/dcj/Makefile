# known aftr running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# auxiliary scripts
DCJ := ../../60-matrix/dcj
BUILD_MATRIX := ../../60-matrix/build_distance_matrix.py
GEN_COMPS := ../../60-matrix/gen_pairwise_comparisons.py
ROOTED_TREE := ../../70-tree/rooted-nj-tree-with-outgroup.R

.PHONY: unimog2pairs clean

%_tree: %_matrix.csv
	${ROOTED_TREE} $< $@ ${OUTGROUP}

dcj_matrix.csv: unimog2pairs
	ls *_vs_*.unimog | parallel --colsep '\t' ./dcjindel.sh {} | tr '\t' ',' | ${BUILD_MATRIX} - > $@

unimog2pairs: ../dummy_data.unimog
	./unimog2pairs.py $<

clean:
	rm -f *.nwk *.unimog *.lp *.sol *.ids *.log *.csv
