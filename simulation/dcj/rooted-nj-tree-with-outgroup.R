#!/usr/bin/env Rscript

library(ape)
library(phangorn)

# args[1] expects the distance matrix in PHYLIP format as provided by triangular2square.awk
# args[2] expects the name for the output file (no extension)
# args[3] expects the label of the outgroup
args <- commandArgs(trailingOnly=TRUE)

mat <- phangorn::readDist(args[1], format="phylip")

tree <- ape::nj(mat)
tree <- ape::root(tree, args[3], resolve.root=TRUE)

write.tree(tree, file=paste(args[2], ".nwk", sep=""))
