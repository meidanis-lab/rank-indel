Run the following:
```bash
ls ../30-pcla | grep '\.pcla' | awk -F. '{OFS="."; print $1,"norep"}' | xargs make
```
