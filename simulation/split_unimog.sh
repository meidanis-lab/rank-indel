#!/usr/bin/bash

# Split Unimog into separate genomes
cat $1 | csplit - '/^>/' '{*}' -s -f genome-

# Remove the first part; it is empty.
rm genome-00

# Rename the files with their respective headers.
# Note that we remove the ">" character. In addition, 
# remove the headers; not necessary for input.
for file in genome-*
do 
    new_name=$(head -1 ${file} | sed -e 's/>//g' -e 's/$/\.txt/g'); 
    sed -i '/^>/d' ${file}
    mv ${file} ${new_name};
done
