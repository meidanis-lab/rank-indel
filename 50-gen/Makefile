DATA := ../45-jackknife/samples
OUTPUT := samples
NSAMPLES := $(shell ls ${DATA} | wc -l)

.PHONY: conversion clean

conversion: ${DATA}
		mkdir ${OUTPUT}
		for i in `seq 1 ${NSAMPLES}`; do \
				mkdir ${OUTPUT}/$${i}; \
				ls $</$${i} | cut -d. -f1 | xargs -I {} ./parse_genomes.py -i $</$${i}/{}.genome -o ${OUTPUT}/$${i}/{}.gen --circular; \
		done

clean:
	rm -rf *.gen samples
