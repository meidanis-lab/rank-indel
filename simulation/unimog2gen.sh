#!/usr/bin/bash

cat $1 | 
    # Recall that Unimog file specify the type of chromosome by the last
    # character in a chromosome line: ")" for circular and "|" for linear.
    # The AWK program below inserts either a "(" or "[" in the beginning
    # of these lines depending on the last character. Note that "|" is 
    # replaced by "]".
    awk '{
        if ($NF == ")") {
            print "( " $0
        } else if ($NF == "|") {
            $NF="]"; 
            print "[ " $0
        } else print
    }' |
    # Split the Unimog file by the lines starting with ">" (those that specify 
    # a name for the genome). 
    csplit - '/^>/' '{*}' -s -f genome-

# Remove the first part; it is empty.
rm genome-00

# Rename the files with their respective headers followed by the ".gen" extension.
# Note that we remove the ">" character. In addition, remove the headers (they are 
# not part of Gen files).
for file in genome-*
do 
    new_name=$(head -1 ${file} | sed -e 's/>//g' -e 's/$/\.gen/g'); 
    sed -i '/^>/d' ${file}
    mv ${file} ${new_name};
done
