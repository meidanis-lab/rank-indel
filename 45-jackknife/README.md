Run the following adjusting `-n` (number of samples) and `-r` (percentage to be removed) as required:
```bash
ls ../40-genome/*.genome | paste -s -d, | xargs -I {} ./jackknife.py -i {} -n 50 -r .5
```
