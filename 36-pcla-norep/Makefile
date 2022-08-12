AMPLICONS := ../30-pcla
REPEATS := ../33-repeats

amplicons_size.txt:
	ls *.norep | xargs wc -l | sort > $@

%.norep: $(AMPLICONS)/%.pcla
	# WARNING: I added the "OR true" at the end in case grep finds no matchings.
	# As of 19-05, V_gazogenes (amplicon 03) has no matching, i.e. ALL genes are repeated.
	# This makes grep exit status be 1, which interrupts the Makefile execution.
	cat $^ | cut -c 2- | grep -Fxvf $(REPEATS)/$(shell echo $* | awk -F '-' '{print $$1 ".repeats"}') | grep -Ff - $^ > $@ || true

clean:
	rm -f *.norep *.txt
