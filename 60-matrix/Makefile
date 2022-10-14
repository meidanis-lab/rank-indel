DATA := ../50-gen/samples
NSAMPLES := $(shell ls ${DATA} | wc -l)

RANK := rank/dist.py 0 0
RANKINDL := rank/dist.py 0 1
RANKC := rank/rank.py

.PHONY: rank_matrix dcj_matrix convert_gen clean

rankc_matrix: rank/samples
	for i in `seq 1 ${NSAMPLES}`; do \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' ${RANKC} {} | tr '\t' ',' | ./build_distance_matrix.py - > rankc_matrix_$${i}.mat; \
	done

rank_matrix: rank/samples
	for i in `seq 1 ${NSAMPLES}`; do \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' ${RANK} {} | tr '\t' ',' | ./build_distance_matrix.py - > rank_matrix_$${i}.mat; \
	done

rankindl_matrix: rank/samples
	for i in `seq 1 ${NSAMPLES}`; do \
		ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' ${RANKINDL} {} | tr '\t' ',' | ./build_distance_matrix.py - > rankindl_matrix_$${i}.mat; \
	done

rank/samples: ${DATA}
	cd rank && $(MAKE)

# need to convert to UniMoG
dcj_matrix: ../45-jackknife/samples
	for i in `seq 1 ${NSAMPLES}`; do \
	    ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' dcj/dcjindel.sh {} | tr '\t' ',' | ./build_distance_matrix.py - > dcj_matrix_$${i}.mat; \
	done

clean:
	rm -f *.unimog *.log *.mat
	cd rank && $(MAKE) clean
	cd dcj && rm -f *.sol *.lp *.ids *.csv *.unimog
