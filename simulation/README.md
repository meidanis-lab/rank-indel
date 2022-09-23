## Shorthand
The pipeline for the rank distance can be easily run as follows:
```bash
make rank_tree
make rankindl_tree
```
The DCJ pipeline, on the other hand, relies on Python 2 in an intermidiate step.
In addition, one must have a working installation of Gurobi 9.5.1.
The steps must be the following:
```bash
conda activate dcj     # activate env with python 2
make dcj_tree
conda deactivate
```

## Detailed steps
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
