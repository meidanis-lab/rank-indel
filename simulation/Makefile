# known after running 'dummy_tree.nwk' with '-r seed'
OUTGRP := L20

# number of taxa
NTAXA := 20

# simulator parameters
INSERTION_RATE := 0.2
DELETION_RATE := 0.4
NGENES := 5000
NCHRS := 2

.PHONY: rank rankc rankindl dcj clean

rank rankc rankindl: dummy_data.unimog
	cd rank && $(MAKE) $@_tree

# WARNING: requires Python 2 and Gurobi
# activate another environment
dcj: dummy_data.unimog
	cd dcj && $(MAKE) $@_tree

dummy_data.unimog: dummy_tree.nwk
	./simulate_dcj.py \
	    -g ${NGENES} \
	    -x ${NCHRS} \
	    -i ${INSERTION_RATE} \
	    -e ${DELETION_RATE} \
	    -l $< 2> simulate_dcj.log > $@

dummy_tree.nwk:
	ngesh -L ${NTAXA} -x enum -r seed > $@

clean:
	rm -f *.nwk *.unimog *.log
	cd rank && $(MAKE) clean
	cd dcj && $(MAKE) clean
