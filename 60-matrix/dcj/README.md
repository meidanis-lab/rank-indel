**Warning:** Two critical dependencies for the proper functioning of this step is python2 and Gurobi.
These are not included in the environment (saved in `spec-file-linux-64`) created for this pipeline and should be handled separately by the user.
We will fix this unfortunate workaround later.

The programs `unimog_to_ilp.py`, `parse_gurobi_sol.py`, and `ilp_utils.py` were taken from https://gitlab.ub.uni-bielefeld.de/gi/ding and described by Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020).

- Bohnenkämper, L., Braga, M.D.V., Doerr, D., Stoye, J. (2020). Computing the Rearrangement Distance of Natural Genomes. In: Schwartz, R. (eds) Research in Computational Molecular Biology. RECOMB 2020. Lecture Notes in Computer Science(), vol 12074. Springer, Cham. [DOI](https://doi.org/10.1007/978-3-030-45257-5_1)
