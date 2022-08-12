#!/usr/bn/env Rscript

library(ape)

args = commandArgs(trailingOnly=TRUE)

mat = read.csv(args[1], header=TRUE, row.names=1)
mat[is.na(mat)] = 0
mat = as.dist(mat)

tree = ape::nj(as.matrix(mat))

write.tree(tree, file=paste(args[2], ".nwk", sep=""))
