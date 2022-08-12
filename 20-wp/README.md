Run the following:
```bash
ls ../10-amplicon | grep gff | awk -F. '{OFS="."; print $1,"wp"}' | xargs make
```
