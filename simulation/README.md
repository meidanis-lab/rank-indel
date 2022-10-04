## Running the pipelines
Each `make` below geneates a phylogenetic tree in Newick format using the distance model specified.
```bash
make rank_tree
make rankindl_tree
make dcj_tree
```

## Parameters of the simulator
The simulator is run with the following parameters by default, but they can be adjusted by the user.
```bash
./simulate_dcj.py -g 5000 -x 2 -i 0.2 -e 0.4 --indel_size_zipf 4 -c -l dummy_tree.nwk 2> simulate_dcj.log > dummy_data.unimog
```
The parameters are the following:
- `-g`: number of genes in root genome;
- `-x`: number of chromosomes in root genome;
- `-i`: insertion rate;
- `-e`: deletion rate;
- `-c`: circular genomes only;
- `-l`: output the leaves only;
- `--indel_size_zipf`: size of indel segment sampled from Zipf distribution.

## References
The programs `simulate_dcj.py` and `trees.py` were taken from https://gitlab.ub.uni-bielefeld.de/gi/ding and described by Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020).

- Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020). Computing the Rearrangement Distance of Natural Genomes. In: Schwartz, R. (eds) Research in Computational Molecular Biology. RECOMB 2020. Lecture Notes in Computer Science(), vol 12074. Springer, Cham. [DOI](https://doi.org/10.1007/978-3-030-45257-5_1)

We also make use of UniMoG, available at http://bibiserv.cebitec.uni-bielefeld.de/dcj, to compute the DCJ-Indel distance.

- Braga, M. D., Willing, E., & Stoye, J. (2011). Double cut and join with insertions and deletions. Journal of computational biology : a journal of computational molecular cell biology, 18(9), 1167–1184. [DOI](https://doi.org/10.1089/cmb.2011.0118)
