Run the following:
```bash
ls ../00-gff | grep gff.gz | awk -F. '{print $1"-01"}' | xargs make
```
