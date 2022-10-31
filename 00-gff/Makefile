CONFIG := ../config

download_%: $(CONFIG)/%.csv
		@# Select column with Accessions Numbers, paste them in a single line separated by commas, and
		@# pass to ncbi-genome-download so that this tool downloads the files in GFF format.
		cat $< | grep -v '^#' | cut -d, -f6 | paste -s -d, | xargs -I {} ncbi-genome-download all --assembly-accessions {} --format gff
		mv refseq/*/GCF*/*.gz .
		rm -r refseq/
		@# Rename GFF files according to annotation in CSV from config directory.
		cat $< | grep -v '^#' | cut -d, -f5,6 | awk -F, '{OFS=" "; print "mv",$$2"*",$$1".gff.gz"}' | bash -

query_%: $(CONFIG)/%.csv
		cat $< | grep -v '^#' | cut -d, -f6 | paste -s -d, | xargs -I {} ncbi-genome-download all --assembly-accessions {} --dry-run

clean:
		rm -f *.gff.gz *.txt
