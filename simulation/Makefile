# known after running 'dummy_tree.nwk' with '-r seed'
OUTGROUP := L20

# number of taxa
NTAXA := 20

# simulator parameters
INSERTION_RATE := 0.2
DELETION_RATE := 0.4
NGENES := 5000
NCHRS := 2
INDEL_SIZE := 4

.PHONY: clean

rank_tree: dummy_data.unimog
	cd rank && $(MAKE) rank_tree

rankindl_tree: dummy_data.unimog
	cd rank && $(MAKE) rankindl_tree

# WARNING: requires Python 2 and Gurobi
# activate another environment
dcj_tree: dummy_data.unimog
	cd dcj && $(MAKE) dcj_tree

dummy_data.unimog: dummy_tree.nwk
	./simulate_dcj.py \
	    -g ${NGENES} \
	    -x ${NCHRS} \
	    -i ${INSERTION_RATE} \
	    -e ${DELETION_RATE} \
	    --indel_size_zipf ${INDEL_SIZE} \
	    -l $< 2> simulate_dcj.log > $@

dummy_tree.nwk:
	ngesh -L ${NTAXA} -x enum -r seed > $@

clean:
	rm -f *.nwk *.unimog *.log
	cd rank && $(MAKE) clean
	cd dcj && $(MAKE) clean
