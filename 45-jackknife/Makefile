DATA := ../40-genome

# default parameters for jackknife
N := 50
R := 0.5

.PHONY: jackknife clean

jackknife: ${DATA}
		ls $</*.genome | paste -s -d, | xargs -I {} ./jackknife.py -i {} -n ${N} -r ${R}

clean:
		rm -rf samples
