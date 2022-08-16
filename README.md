## Rank distance for real data
To generate the results for the Rank distances, run the following:
```bash
conda create --name rank --file spec-file-linux-64     # create conda env from spec file
conda activate rank                                    # activate env
make esche_shige OUTGROUP=E_ferg_ATCC35469T N=1 R=0    # run pipeline for rank distances
```
The outputs are the Newick files containing the phylogenetic trees.

The code to generate the figures and comparison metrics is available in the jupyter notebook `70-tree/analysis.ipynb`.

## DCJ-Indel distance for real data
:warning: **Requires Python 2 and Gurobi**
To generate the results for the DCJ-Indel distance, run the following:
```
cd 60-matrix
make dcj_matrix
cd ../70-tree
make dcj_nj_rooted_tree
```
The outputs are the Newick files containing the phylogenetic trees.

The code to generate the figures and comparison metrics is available in the jupyter notebook `70-tree/analysis.ipynb`.

## Rank and DCJ-Indel distances for simulated data
See the folder `simulation`.
