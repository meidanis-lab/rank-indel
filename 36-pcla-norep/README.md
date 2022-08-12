Run the following:
```bash
ls ../30-pcla | grep '\.pcla' | awk -F. '{OFS="."; print $1,"norep"}' | xargs make
```

UPDATE (19-05):
Amplicon 3 do *V. gazogenes* está quebrando o make.
Pela saída, o arquivo norep do amplicon 3 está vazio.
Então TODOS os genes são reptidos? 
Parece que sim...
Isso faz o exit status do grep ser 1, o que interrompe a execução do make.
Coloquei `|| true` no final para que o exit status seja sempre 0.
