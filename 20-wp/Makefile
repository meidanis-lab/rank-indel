%.wp: ../10-amplicon/%.gff
	# 1) Extract orientation of gene along with the 'attribute' field;
	# 2) Extract the first tag from the semicolon-separated list of tag-value pairs in the 'attribute' field;
	# 3) Filter those that contain contain WP;
	# 4) Leave just orientation and gene ID.
	# Idea for later: extract Name tag from 'attribute' field; it already has the gene annotation.
	cat $< | cut -f7,9 | cut -d ';' -f1 | grep WP_ | sed 's/\([+-]\)\t.*\(WP_[0-9]*\.[0-9]\).*/\1\2/' > $@

clean:
	rm -f *.wp
