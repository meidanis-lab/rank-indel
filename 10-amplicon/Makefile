%-01: ../00-gff/%.gff.gz
	gunzip < $< | csplit -b '%02d.gff' -f '$*-' - '/	region	\|I	CoGe	chromosome/' '{*}'
	rm $*-00.gff
	@# remove plasmids
	@#ls $** | grep -e '\-01.gff' -e '\-02.gff' -v | xargs rm -f

clean:
	rm -f *.gff
