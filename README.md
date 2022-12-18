## Dependencies
Step `20-wp` requires the `PCLA_proteins.txt.gz` file, which contains the protein clusters.
The pipeline will download this file automatically as follows:
```bash
wget --no-check-certificate http://www.ic.unicamp.br/~meidanis/PUB/Mestrado/2020-Oliveira/PCLA_proteins.txt.gz && mv PCLA_proteins.txt.gz 20-wp
```
We provide a specification file `spec-file-linux-64` to replicate our environment.
Nevertheless, these are the required packages to run the pipeline:
```bash
conda install -c conda-forge r-base
conda install -c conda-forge r-ape
conda install -c conda-forge r-codetools
conda install -c conda-forge jupyterlab
conda install -c bioconda r-phangorn
conda install -c bioconda ncbi-genome-download
conda install -c bioconda bioconductor-ggtree
conda install -c r r-irkernel
```
In addition, install the `Quartet` package by typing `install.packages('Quartet')` from within R.
(Note that the `quartet` package available in Conda is *not* the same.)

## Generating the results
To generate the results for a rearrangement distance, run the following:
```bash
conda create --name my_env --file spec-file-linux-64      # create conda env from spec file
conda activate my_env                                     # activate env
make esche_shige DIST=${DIST} OUTGRP=EF_ATCC35          # run pipeline for rank distances
```
Here, ${DIST} is either `rank`, `rankindl`, `rankc`, or `dcj`.
For the rank distance, we recommend using `rankc`, which is more efficient than the other two.
The outputs are the Newick files containing the phylogenetic trees in `70-tree`.
The code to generate the figures and comparison metrics is available in the jupyter notebook `70-tree/analysis.ipynb`.

## Pipeline for *Shigella* and *E. coli* species
Running `make` will display a helper message on options for the parameters.
A required dependency for the proper execution of the pipeline is the content in the `config` folder:
- `test.csv`: metadata of 4 *Vibrio* strains used for testing purposes;
 - `OUTGRP=AS\_VS224`
- `esche_shige.csv`: metadata of *Shigela* and *E. coli* genomes, e.g. accession number, annotation, etc;
 - `OUTGRP=EF_ATCC35`
- `esche_shige_short.tree`: reference phylogenetic tree.

## Pipeline for simulated data
See the folder `simulation`.
