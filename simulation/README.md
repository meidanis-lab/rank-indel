## Running the pipelines
The pipeline for the rank distance can be run as follows:
```bash
make rank_tree
make rankindl_tree
```
The DCJ pipeline relies on Python 2 in an intermediate step.
In addition, one must have a working installation of Gurobi 9.5.1.
The steps must be the following:
```bash
conda activate dcj     # activate env with python 2
make dcj_tree
conda deactivate
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

## Measuring performance
The performance measure should be done when the distance is computed.
After having generated the Gen files, run the following:
```bash
ls *.gen | xargs ../60-matrix/gen_pairwise_comparisons.py > comparisons.txt
time cat comparisons.txt | parallel --colsep '\t' ${DIST} {}
```
where `DIST` is the script that computes a rearrangement distance.

## References
The programs `simulate_dcj.py` and `trees.py` were taken from https://gitlab.ub.uni-bielefeld.de/gi/ding and described by Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020).

- Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020). Computing the Rearrangement Distance of Natural Genomes. In: Schwartz, R. (eds) Research in Computational Molecular Biology. RECOMB 2020. Lecture Notes in Computer Science(), vol 12074. Springer, Cham. [DOI](https://doi.org/10.1007/978-3-030-45257-5_1)
