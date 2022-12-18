CONFIG := config
DIST := rankc
OUTGRP := ""

# default parameters for jackknife
N := 1
R := 0

.PHONY: usage 00-gff 10-amplicon 20-wp 30-pcla 33-repeats 36-pcla-norep 40-genome 45-jackknife 50-gen 60-matrix 70-tree

usage:
	@echo "Usage: make [esche_shige | test]"
	@echo "Required variables:"
	@echo "\tDIST,\tdistance model, one of [rank | rankc | rankindl | dcj] (default: DIST=rank)"
	@echo "\tOUTGRP,\tannotation of outgroup organism] (see CSV in config folder, e.g. OUTGRP=AS_VS224)"
	@echo "Optional variables:"
	@echo "\tN,\tnumber of samples for jeckknife (default: N=1)"
	@echo "\tR,\tfloat between 0.0 and 1.0 for jackknife rate (default: R=0)"

query_%: $(CONFIG)/%.csv
	$(MAKE) -C 00-gff $@

%: $(CONFIG)/%.csv
	$(MAKE) -C 00-gff download_$@
	$(MAKE) 70-tree

70-tree: 60-matrix
	$(MAKE) -C $@ ${DIST}_nj_rooted_tree OUTGRP=${OUTGRP}

60-matrix: 50-gen
	$(MAKE) -C $@ ${DIST}

50-gen: 45-jackknife
	$(MAKE) -C $@

45-jackknife: 40-genome
	$(MAKE) -C $@ N=${N} R=${R}

40-genome: 36-pcla-norep
	cd $@ && ls ../$< | grep '\.norep' | awk -F- '{OFS="."; print $$1,"genome"}' | xargs $(MAKE)

36-pcla-norep: 30-pcla 33-repeats
	cd $@ && ls ../$< | grep '\.pcla' | awk -F. '{OFS="."; print $$1,"norep"}' | xargs $(MAKE) && $(MAKE)

33-repeats: 30-pcla
	cd $@ && ls ../$< | grep '\.pcla' | awk -F- '{OFS="."; print $$1,"repeats"}' | xargs $(MAKE)

30-pcla/PCLA_proteins.txt.gz:
	wget --no-check-certificate https://www.ic.unicamp.br/~meidanis/PUB/Mestrado/2020-Oliveira/PCLA_proteins.txt.gz
	mv PCLA_proteins.txt.gz $@

30-pcla: 20-wp 30-pcla/PCLA_proteins.txt.gz
	cd $@ && zcat PCLA_proteins.txt.gz | ./wp2pcla.py - $$(ls ../$</* | grep '\.wp')

20-wp: 10-amplicon
	cd $@ && ls ../$< | grep gff | awk -F. '{OFS="."; print $$1,"wp"}' | xargs $(MAKE)

10-amplicon: 00-gff
	cd $@ && ls ../$< | grep gff.gz | awk -F. '{print $$1"-01"}' | xargs $(MAKE)

clean:
	cd 00-gff && $(MAKE) clean
	cd 10-amplicon && $(MAKE) clean
	cd 20-wp && $(MAKE) clean
	cd 30-pcla && $(MAKE) clean
	cd 33-repeats && $(MAKE) clean
	cd 36-pcla-norep && $(MAKE) clean
	cd 40-genome && $(MAKE) clean
	cd 45-jackknife && $(MAKE) clean
	cd 50-gen && $(MAKE) clean
	cd 60-matrix && $(MAKE) clean
	cd 70-tree && $(MAKE) clean
