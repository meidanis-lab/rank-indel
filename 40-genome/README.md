Run the following:
```bash
ls ../36-pcla-norep | grep '\.norep' | awk -F- '{OFS="."; print $1,"genome"}' | xargs make
```
