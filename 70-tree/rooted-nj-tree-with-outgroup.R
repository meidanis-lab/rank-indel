#!/usr/bin/env Rscript

library(ape)
library(phangorn)

# args[1] expects the distance matrix format specified by args[4]
# args[2] expects the name for the output file (no extension)
# args[3] expects the label of the outgroup
# args[4] 'csv' or 'phylip' (as provided by 'triangular2square.awk')
args <- commandArgs(trailingOnly=TRUE)

if (args[4] == "csv") {
    mat <- read.csv(args[1], header=TRUE, row.names=1)
    mat[is.na(mat)] <- 0
    mat <- as.matrix(as.dist(mat))
} else if (args[4] == "phylip") {
    mat <- phangorn::readDist(args[1], format="phylip")
} else {
    stop("matrix format must be either 'csv' or 'phylip'")
}

tree <- ape::nj(mat)
tree <- ape::root(tree, args[3], resolve.root=TRUE)

write.tree(tree, file=paste(args[2], ".nwk", sep=""))
