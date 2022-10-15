DATA := ../50-gen/samples
NSAMPLES := $(shell ls ${DATA} | wc -l)

RANK := rank/dist.py 0 0
RANKINDL := rank/dist.py 0 1
RANKC := rank/rank.py
UNIMOG := unimog/UniMoG-java11.jar

.PHONY: rankc_matrix rank_matrix rankindl_matrix dcj_matrix convert_gen clean

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

rank/samples:
	cd rank && $(MAKE)

#dcj_matrix:
#	for i in `seq 1 ${NSAMPLES}`; do \
#	    ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' ding/dcjindel.sh {} | tr '\t' ',' | ./build_distance_matrix.py - > dcj_matrix_$${i}.mat; \
#	done

## TODO: Fix egrep and organisms names; these are causing trouble when converting the matrix.
dcj_matrix: unimog/samples
	for i in `seq 1 ${NSAMPLES}`; do \
	    java -jar ${UNIMOG} -m=6 -d $</$${i}/genomes.unimog | egrep -e "^L[0-9]{2}" -e "^[0-9]{2}" | unimog/triangular2square.awk > dcj_matrix_$${i}.mat; \
	done

unimog/samples:
	cd unimog && $(MAKE)

clean:
	rm -f *.unimog *.log *.mat
	cd rank && $(MAKE) clean
	cd ding && rm -f *.sol *.lp *.ids *.csv *.unimog
	cd unimog && $(MAKE) clean
