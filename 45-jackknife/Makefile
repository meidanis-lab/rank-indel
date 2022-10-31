DATA := ../40-genome

# default parameters for jackknife
N := 1
R := 0

.PHONY: jackknife clean

jackknife: ${DATA}
		ls $</*.genome | paste -s -d, | xargs -I {} ./jackknife.py -i {} -n ${N} -r ${R}

clean:
		rm -rf samples
