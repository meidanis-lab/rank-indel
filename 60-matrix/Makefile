DATA := ../50-gen/samples
NSAMPLES := $(shell ls ${DATA} | wc -l)

.PHONY: rank_matrix dcj_matrix clean

rank_matrix: ${DATA}
	for i in `seq 1 ${NSAMPLES}`; do \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' rank/rankindel.py {} | tr '\t' ',' | ./build_distance_matrix.py - > rank_matrix_$${i}.csv; \
	done

dcj_matrix: ../45-jackknife/samples
	for i in `seq 1 ${NSAMPLES}`; do \
	    ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' dcj/dcjindel.sh {} | tr '\t' ',' | ./build_distance_matrix.py - > dcj_matrix_$${i}.csv; \
	done

clean:
	rm -f *.csv
	cd dcj && rm -f *.sol *.lp *.ids *.csv *.unimog
