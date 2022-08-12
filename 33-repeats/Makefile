DATA := ../30-pcla

%.repeats: $(DATA)/%-01.pcla
	cat $(DATA)/$*-* | cut -c 2- | sort | uniq -c | sort -r | grep -v "1 " | cut -c 9- > $@

clean:
	rm -f *.repeats
