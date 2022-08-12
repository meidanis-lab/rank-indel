SHELL := /bin/bash
DATA := ../36-pcla-norep

%.genome: $(DATA)/%-01.norep
	cp /dev/null $@
	for i in `ls $(DATA)/$*-*`; do \
	  tr '\n' ' ' < $$i | cat - <(echo) >> $@; \
	done

clean:
	rm -f *.genome
