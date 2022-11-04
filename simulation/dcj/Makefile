# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# outfile for 'time' that will record the running time
TIME := "timing.txt"

# auxiliary scripts
UNIMOG := ../../60-matrix/unimog/UniMoG-java11.jar
BUILD_MATRIX := ../../60-matrix/build_distance_matrix.py

.PHONY: clean

%_tree: %_matrix.mat
	./rooted-nj-tree-with-outgroup.R $< $@ ${OUTGROUP}

#dcj_matrix.mat: unimog2pairs
#	ls *_vs_*.unimog | \time -a -f "%e" -o ${TIME} parallel ./dcjindel.sh {} | tr '\t' ',' | ${BUILD_MATRIX} - > $@

#unimog2pairs: ../dummy_data.unimog
#	./unimog2pairs.py $<

dcj_matrix.mat: ../dummy_data.unimog
	\time -a -f "%e" -o ${TIME} java -jar ${UNIMOG} -m=6 -d $< | egrep -e "^L[0-9]{2}" -e "^[0-9]{2}" | ./triangular2square.awk > $@

clean:
	rm -f *.nwk *.unimog *.lp *.sol *.ids *.log *.csv *.mat
