# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# auxiliary scripts
UNIMOG := ../../60-matrix/dcj/UniMoG-java11.jar
BUILD_MATRIX := ../../60-matrix/build_distance_matrix.py
GEN_COMPS := ../../60-matrix/gen_pairwise_comparisons.py
ROOTED_TREE := ../../70-tree/rooted-nj-tree-with-outgroup.R

.PHONY: unimog2pairs clean

%_tree: %_matrix.mat
	./rooted-nj-tree-with-outgroup.R $< $@ ${OUTGROUP}
#	${ROOTED_TREE} $< $@ ${OUTGROUP}

#dcj_matrix.mat: unimog2pairs
#	ls *_vs_*.unimog | parallel --colsep '\t' ./dcjindel.sh {} | tr '\t' ',' | ${BUILD_MATRIX} - > $@

#unimog2pairs: ../dummy_data.unimog
#	./unimog2pairs.py $<

dcj_matrix.mat: ../dummy_data.unimog
	java -jar ${UNIMOG} -m=6 -d $< | egrep -e "^L[0-9]{2}" -e "^[0-9]{2}" | ./triangular2square.awk > $@

clean:
	rm -f *.nwk *.unimog *.lp *.sol *.ids *.log *.csv
