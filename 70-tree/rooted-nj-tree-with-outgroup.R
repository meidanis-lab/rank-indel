#!/usr/bin/env Rscript

library(ape)
#library(ggtree)

# args[1] expects the distance matrix in CSV format as provided by 60-matrix
# args[2] expects the name for the output file (no extension)
# args[3] expects the label of the outgroup
args = commandArgs(trailingOnly=TRUE)

mat = read.csv(args[1], header=TRUE, row.names=1)
mat[is.na(mat)] = 0
mat = as.dist(mat)

tree = ape::nj(as.matrix(mat))
tree = ape::root(tree, args[3], resolve.root=TRUE)

write.tree(tree, file=paste(args[2], ".nwk", sep=""))

# This step will be done in an interactive session (e.g. jupyter notebook)
# png(filename=paste(args[2], ".png", sep=""))
# plot = ggtree(tree, branch.length="none", layout="circular") + 
#         geom_tiplab() + 
#         theme(plot.margin=unit(c(50,44,50,44),"mm"))
# print(plot)
# dev.off()
