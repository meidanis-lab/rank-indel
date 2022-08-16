## Real data
To generate the results for the Rank distances, run the following:
```bash
conda create --name rank --file spec-file-linux-64     # create conda env from spec file
conda activate rank                                    # activate env
make esche_shige OUTGROUP=E_ferg_ATCC35469T N=1 R=0    # run pipeline for rank distances
```
As for the DCJ-Indel distance, **Python 2** and **Gurobi 9.5.1** are required dependencies.
These are *not* included in the `spec-file-linux-64` file.
Since Gurobi is a proprietary software, its installation must be handled separately.
Hence, steps `60-matrix` and `70-tree` have to be run manually for this distance as follows:
```
cd 60-matrix
make dcj_matrix
cd ../70-tree
make dcj_nj_rooted_tree
```
The outputs are the Newick files containing the phylogenetic trees in `70-tree`.
The code to generate the figures and comparison metrics is available in the jupyter notebook `70-tree/analysis.ipynb`.

## Rank and DCJ-Indel distances for simulated data
See the folder `simulation`.
