Download the following file:
```bash
wget http://www.ic.unicamp.br/~meidanis/PUB/Mestrado/2020-Oliveira/PCLA_proteins.txt.gzs
```

Run the following:
```bash
zcat PCLA_proteins.txt.gz | ./wp2pcla.py - $(ls ../20-wp/* | grep '\.wp')
```
