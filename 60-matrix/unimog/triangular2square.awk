#!/usr/bin/awk -f
#
# Converts a lower triangular PHYLIP matrix to a square PHYLIP matrix.
# Source: http://giphy.pasteur.fr/faq/phylogenetics/distance-matrix-file-conversion/

NR>1 {
    (m < (l = length(lbl[++n] = $(c = j = 1)))) && m = l;
    --j;
    while (++c <= n)
        d[j][n] = d[n][(++j)] = $c
}

END {
    print (b = " ") n;
    x = 0.5;
    while ((x *= 2) < m) 
        b = b "" b;
    z = substr("0.0000000000000000000", 1, length(d[1][2]));
    while (++i <= n) {
        d[i][i]=z;
        printf substr(lbl[i]b, 1, m);
        j = 0;
        while (++j <= n)
            printf " " d[i][j];
        print ""
    }
}
