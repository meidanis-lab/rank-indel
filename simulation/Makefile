# known after running 'dummy_tree.nwk' with '-r seed'
OUTGRP := L20

# output file for 'time' for running time measurement
TIME := "timing.txt"

# number of taxa
NTAXA := 20

# simulator parameters
INSRATE := 0.2
DELRATE := 0.4
NGENES := 5000
NCHRS := 2

.PHONY: rank rankc rankindl dcj clean usage

usage:
	@echo "Usage: make [rank | rankindl | rankc | dcj]" 
	@echo "Required variables:"
	@echo "\tTIME,\t\tfile where running time of program computing distance will be recorded (default: TIME=timing.txt)"
	@echo "\t\t\tnote that the output of multiple runs will be appended in the same file"
	@echo "Optional variables:"
	@echo "\tNTAXA,\t\tnumber of leaf genomes for phylogenetic tree (default: NTAXA=20)"
	@echo "\tNGENES,\t\tnumber of genes per genome (default: NGENES=5000)"
	@echo "\tNCHRS,\t\tnumber of chromosomes per genome (default: NCHRS=2)"
	@echo "\tINSRATE,\trate of insertion events (default: INSRATE=0.2)"
	@echo "\tDELRATE,\trate of deletion events (default: DELRATE=0.4)"

rank rankc rankindl: dummy_data.unimog
	cd rank && $(MAKE) $@_tree TIME=${TIME}

# WARNING: requires Python 2 and Gurobi
# activate another environment
dcj: dummy_data.unimog
	cd dcj && $(MAKE) $@_tree TIME=${TIME}

dummy_data.unimog: dummy_tree.nwk
	./simulate_dcj.py \
	    -g ${NGENES} \
	    -x ${NCHRS} \
	    -i ${INSRATE} \
	    -e ${DELRATE} \
	    -l $< 2> simulate_dcj.log > $@

dummy_tree.nwk:
	ngesh -L ${NTAXA} -x enum -r seed > $@

clean:
	rm -f *.nwk *.unimog *.log
	cd rank && $(MAKE) clean
	cd dcj && $(MAKE) clean
