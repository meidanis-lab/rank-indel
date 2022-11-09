## Quick start
To generate the results for the Rank distances, run the following:
```bash
conda create --name rank --file spec-file-linux-64      # create conda env from spec file
conda activate rank                                     # activate env
make esche_shige DIST=rankc OUTGROUP=E_ferg_ATCC35469T  # run pipeline for rank distances
```
The outputs are the Newick files containing the phylogenetic trees in `70-tree`.
The code to generate the figures and comparison metrics is available in the jupyter notebook `70-tree/analysis.ipynb`.

## Pipeline for *Shigella* and *E. coli* species
Running `make` will display a helper message on options for the parameters.
A required dependency for the proper execution of the pipeline is the content in the `config` folder:
- `test.csv`: metadata of 4 *Vibrio* strains used for testing purposes;
- `esche_shige.csv`: metadata of *Shigela* and *E. coli* genomes, e.g. accession number, annotation, etc;
- `esche_shige.tree`: reference phylogenetic tree.

## Pipeline for simulated data
See the folder `simulation`.
