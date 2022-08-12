DATA := ../../50-gen/samples
OUTPUT := samples
NSAMPLES := $(shell ls ${DATA} | wc -l)
NGENOMES := $(shell ls ${DATA}/1 | wc -l)

.PHONY: clean convert

convert: ${DATA}
	mkdir -p ${OUTPUT}
	for i in `seq 1 ${NSAMPLES}`; do \
		mkdir -p ${OUTPUT}/$${i}; \
		for gen in `ls ${DATA}/$${i} | cut -d. -f1`; do \
			./gen2txt.sh ${DATA}/$${i}/$${gen}.gen > ${OUTPUT}/$${i}/$${gen}.txt; \
		done \
	done

clean:
	rm -rf samples
