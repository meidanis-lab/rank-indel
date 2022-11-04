DATA := ../../50-gen/samples
OUTPUT := samples
NSAMPLES := $(shell ls ${DATA} | wc -l)
NGENOMES := $(shell ls ${DATA}/1 | wc -l)

.PHONY: clean convert

convert: ${DATA}
	mkdir -p ${OUTPUT}
	for i in `seq 1 ${NSAMPLES}`; do \
		mkdir -p ${OUTPUT}/$${i}; \
		ls ${DATA}/$${i}/* | parallel ./gen2unimog.py {} > ${OUTPUT}/$${i}/genomes.unimog; \
	done

clean:
	rm -rf samples
