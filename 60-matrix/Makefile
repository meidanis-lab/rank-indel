DATA := ../50-gen/samples
NSAMPLES := $(shell ls ${DATA} | wc -l)

RANK := rank/dist_rank.sh
RANKINDL := rank/dist_rankindl.sh
RANKC := rank/rank.py
UNIMOG := unimog/UniMoG-java11.jar

.PHONY: dcj rank rankc rankindl convert_gen clean

rank: ${RANK}
rankc: ${RANKC}
rankindl: ${RANKINDL}
rank rankc rankindl:
	cd rank && $(MAKE)
	for i in `seq 1 ${NSAMPLES}`; do \
		ls rank/samples/$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' $< {} | tr '\t' ',' | ./build_distance_matrix.py - > $@_matrix_$${i}.mat; \
	done

dcj: ${DATA}
	for i in `seq 1 ${NSAMPLES}`; do \
	    ls $</$${i}/* | xargs ./gen_pairwise_comparisons.py | parallel --colsep '\t' ding/dcjindel.sh {} | tr '\t' ',' | ./build_distance_matrix.py - > $@_matrix_$${i}.mat; \
	done

## TODO: Fix egrep and organisms names; these are causing trouble when converting the matrix.

#dcj_matrix: unimog/samples
#	for i in `seq 1 ${NSAMPLES}`; do \
#	    java -jar ${UNIMOG} -m=6 -d $</$${i}/genomes.unimog | egrep -e "^L[0-9]{2}" -e "^[0-9]{2}" | unimog/triangular2square.awk > dcj_matrix_$${i}.mat; \
#	done

#unimog/samples:
#	cd unimog && $(MAKE)

clean:
	rm -f *.unimog *.log *.mat
	cd rank && $(MAKE) clean
	cd ding && rm -f *.sol *.lp *.ids *.csv *.unimog
	cd unimog && $(MAKE) clean
