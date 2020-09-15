muestras = open("aRevisarDef.txt").readlines()

corregidas = open("preguntasSQuAD_eu.txt").readlines()

for i in range(len(muestras)):
    if muestras[i] != "1\n":
        corregidas[i] = muestras[i]

with open("preguntasSQuAD_eu_Def.txt", "w") as f:
    for c in corregidas:
        f.write(c)