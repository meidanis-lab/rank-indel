MAP := PCLA_proteins.txt.gz

%.pcla: ../20-wp/%.wp
	zcat $(MAP) | ./wp2pcla.py - $< > $@

clean:
	rm -f *.pcla
