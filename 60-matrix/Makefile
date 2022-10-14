DATA := ../50-gen/samples
NSAMPLES := $(shell ls ${DATA} | wc -l)

RANK := rank/rank.py
#RANK := rank/dist.py 0 0
RANKINDL := rank/dist.py 0 1

.PHONY: rank_matrix dcj_matrix clean

rank_matrix: ${DATA}
	cd rank && $(MAKE)
	for i in `seq 1 ${NSAMPLES}`; do \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' ${RANK} {} | tr '\t' ',' | ./build_distance_matrix.py - > rank_matrix_$${i}.mat; \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' ${RANKINDL} {} | tr '\t' ',' | ./build_distance_matrix.py - > rankindl_matrix_$${i}.mat; \
	done

dcj_matrix: ../45-jackknife/samples
	for i in `seq 1 ${NSAMPLES}`; do \
	    ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' dcj/dcjindel.sh {} | tr '\t' ',' | ./build_distance_matrix.py - > dcj_matrix_$${i}.mat; \
	done

clean:
	rm -f *.csv *.unimog *.log
	cd rank && $(MAKE) clean
	cd dcj && rm -f *.sol *.lp *.ids *.csv *.unimog
