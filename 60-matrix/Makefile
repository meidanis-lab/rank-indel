DATA := ../50-gen/samples
NSAMPLES := $(shell ls ${DATA} | wc -l)

.PHONY: rank_matrix dcj_matrix clean

rank_matrix: ${DATA}
	cd rank && $(MAKE)
	# TODO: refactor duplicated code.
	for i in `seq 1 ${NSAMPLES}`; do \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' rank/dist.py 0 0 {} | tr '\t' ',' | ./build_distance_matrix.py - > rank_matrix_$${i}.csv; \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' rank/dist.py 0 1 {} | tr '\t' ',' | ./build_distance_matrix.py - > rankindl_matrix_$${i}.csv; \
	done

dcj_matrix: ../45-jackknife/samples
	for i in `seq 1 ${NSAMPLES}`; do \
	    ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' dcj/dcjindel.sh {} | tr '\t' ',' | ./build_distance_matrix.py - > dcj_matrix_$${i}.csv; \
	done

clean:
	rm -f *.csv
	cd rank && $(MAKE) clean
	cd dcj && rm -f *.sol *.lp *.ids *.csv *.unimog
