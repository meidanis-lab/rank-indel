CONFIG := config
OUTGROUP := ""

# default parameters for jackknife
N := 50
R := 0.5

.PHONY: usage 00-gff 10-amplicon 20-wp 30-pcla 33-repeats 36-pcla-norep 40-genome 45-jackknife 50-gen 60-matrix 70-tree

usage:
	@echo "Usage: make [esche_shige | test] [OUTGROUP= annotation of outgroup organism] [N= number of samples (default: 50)] [R= float between 0.0 and 1.0 for jackknife rate (default: 0.5)]"

query_%: $(CONFIG)/%.csv
	cd 00-gff && $(MAKE) $@

%: $(CONFIG)/%.csv
	cd 00-gff && $(MAKE) download_$@
	$(MAKE) 70-tree

70-tree: 60-matrix
	cd $@ && $(MAKE) rank_lucas_nj_rooted_tree OUTGROUP=${OUTGROUP} && $(MAKE) rank_joao_nj_rooted_tree OUTGROUP=${OUTGROUP} && $(MAKE) rankindl_joao_nj_rooted_tree OUTGROUP=${OUTGROUP}
	# TODO: add later because now it depends on Gurobi and Python 2
	# cd $@ && $(MAKE) dcj_nj_rooted_tree OUTGROUP=${OUTGROUP}

60-matrix: 50-gen
	cd $@ && $(MAKE) rank_lucas_matrix && $(MAKE) rank_joao_matrix
	# TODO: add later because now it depends on Gurobi and Python 2
	# cd $@ && $(MAKE) dcj_matrix

50-gen: 45-jackknife
	cd $@ && $(MAKE)

45-jackknife: 40-genome
	cd $@ && $(MAKE) N=${N} R=${R}

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
