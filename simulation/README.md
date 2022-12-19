## Running the pipelines
Each `make` below generates a phylogenetic tree in Newick format using the distance model specified.
```bash
make rank
make rankindl
make rankc
make dcj
```
For the rank distance, we recommend `rankc`, which is more efficient than the other two.

## Parameters of the simulator
The simulator is run with the following parameters by default, but they can be adjusted by the user.
```bash
./simulate_dcj.py -g 5000 -x 20 -i 0.2 -e 0.4 -l dummy_tree.nwk 2> simulate_dcj.log > dummy_data.unimog
```
The parameters are the following:
- `-g`: number of genes in root genome;
- `-x`: number of chromosomes in root genome;
- `-i`: insertion rate;
- `-e`: deletion rate;
- `-l`: output the leaves only;

## Performance measurement
When running the Makefile for a particular distance model, we use the program `time` to measure the running time of the program that computes the distance.
By default, this measurement will be recorded in the `timing.txt` file, but one can change this behavior by specifying, for instance, `TIME=another_timing.txt` when running the Makefile.

We ran the following command to measure the running time of our programs:
```bash
for i in `seq 5000 5000 50000`; do make -B ${DIST} NGENES=${i} TIME=${DIST}_timing.txt; done
```
where `${DIST}` is either `rank`, `rankindl`, `rankc`, or `dcj`.
The `${DIST}_timing.txt` file can be loaded in the `analysis.ipynb` notebook in order to generate a dot plot.

## Experiment with *indel* rate
The script `experiment_indel_rate` contains the steps for an experiment that varies the insertion (`-i`) and deletion (`-d`) rates of the simulator.
The other parameters are fixed.
Upon completion, the script will have generated 100 trees, 10 for each value of *indel* rate (`-i` and `-d`) from 0.0 to 0.9, in steps of 0.1.
These results can be loaded in the `analysis.ipynb` notebook in order to generate box plots.

## References
The programs `simulate_dcj.py` and `trees.py` were taken from https://gitlab.ub.uni-bielefeld.de/gi/ding and described by Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020).

- Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020). Computing the Rearrangement Distance of Natural Genomes. In: Schwartz, R. (eds) Research in Computational Molecular Biology. RECOMB 2020. Lecture Notes in Computer Science(), vol 12074. Springer, Cham. [DOI](https://doi.org/10.1007/978-3-030-45257-5_1)

We also make use of UniMoG, available at http://bibiserv.cebitec.uni-bielefeld.de/dcj, to compute the DCJ-Indel distance, since it performs better than the above when there are no repeated markers.

- Braga, M. D., Willing, E., & Stoye, J. (2011). Double cut and join with insertions and deletions. Journal of computational biology : a journal of computational molecular cell biology, 18(9), 1167–1184. [DOI](https://doi.org/10.1089/cmb.2011.0118)
