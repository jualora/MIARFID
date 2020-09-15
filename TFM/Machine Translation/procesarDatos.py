## COGER LAS FRASES DE LOS DATASETS ##

import os
from translate.storage.tmx import tmxfile

def palabras(x):
    return (x[0].split(' '), x[1].split(' '))

for base, dirs, files in os.walk("./Corpus/en-es"):
    datasets = files

j = 1
for dataset in datasets:
    print("Procesando dataset número %d" % j)

    frasesDef = []
    frases = []

    data_path = "./Corpus/en-es/"+dataset

    with open(data_path, 'rb') as fin:
        tmx_file = tmxfile(fin, 'en', 'es')

    for node in tmx_file.unit_iter():
        frases.append((node.getsource(), node.gettarget()))
    
    frasesPal = list(map(lambda x:palabras(x), frases))

    frasesBuenas = [x for x in frasesPal if len(x[0])<=20 and len(x[1])<=20]

    if len(frasesBuenas) < 40000:
        frasesDef += frasesBuenas
    else:
        frasesDef += frasesBuenas[:40000]

    frasesProc = []
    for frase in frasesDef:
        fraseEn = frase[0]
        fraseEs = frase[1]
        frasesProc.append((' '.join(fraseEn), ' '.join(fraseEs)))

    resEn = ''
    resEs = ''

    for frase in frasesProc:
        resEn += frase[0]
        resEs += frase[1]
        if frase is not frasesProc[-1]:
            resEn += '\n'
            resEs += '\n'

    with open("./ParaProcesar/source/frases"+str(j)+".en", "w") as f:
        f.write(resEn)

    with open("./ParaProcesar/target/frases"+str(j)+".es", "w") as f:
        f.write(resEs)

    j+=1

## UNIR LAS FRASES ESCOGIDAS EN UN MISMO FICHERO ##

for base, dirs, files in os.walk("./ParaProcesar/source"):
    datasetsEn = files
for base, dirs, files in os.walk("./ParaProcesar/target"):
    datasetsEs = files

resEn = ""
resEs = ""

for i in range(len(datasetsEn)):
    frases = open("./ParaProcesar/source/"+datasetsEn[i]).readlines()
    for frase in frases:
        resEn += frase

for i in range(len(datasetsEs)):
    frases = open("./ParaProcesar/target/"+datasetsEs[i]).readlines()
    for frase in frases:
        resEs += frase

with open("./ParaProcesar/frases.en", "w") as f:
    f.write(resEn)

with open("./ParaProcesar/frases.es", "w") as f:
    f.write(resEs)


## SEPARAR LAS MUESTRAS EN TRAIN, DEV Y TEST ##

import sys

nTrain = int(sys.argv[1])

frasesEn = open('./ParaProcesar/frases.en').readlines()
frasesEs = open('./ParaProcesar/frases.es').readlines()

frasesTrainEn = frasesEn[:nTrain]
frasesTrainEs = frasesEs[:nTrain]
frasesDevEn = frasesEn[nTrain:nTrain+1000]
frasesDevEs = frasesEs[nTrain:nTrain+1000]
frasesTestEn = frasesEn[nTrain+1000:nTrain+2000]
frasesTestEs = frasesEs[nTrain+1000:nTrain+2000]

resInputTrain = ""
resOutputTrain = ""
resInputDev = ""
resOutputDev = ""
resInputTest = ""
resOutputTest = ""

for frase in frasesTrainEn:
    resInputTrain += frase
    if frase[-1] != '\n':
        resInputTrain += '\n'

for frase in frasesTrainEs:
    resOutputTrain += frase
    if frase[-1] != '\n':
        resOutputTrain += '\n'

for frase in frasesDevEn:
    resInputDev += frase
    if frase[-1] != '\n':
        resInputDev += '\n'

for frase in frasesDevEs:
    resOutputDev += frase
    if frase[-1] != '\n':
        resOutputDev += '\n'

for frase in frasesTestEn:
    resInputTest += frase
    if frase[-1] != '\n':
        resInputTest += '\n'

for frase in frasesTestEs:
    resOutputTest += frase
    if frase[-1] != '\n':
        resOutputTest += '\n'

with open("./datasets/500K_20w_s/en-es/train.en", "w") as f:
    f.write(resInputTrain)

with open("./datasets/500K_20w_s/en-es/train.es", "w") as f:
    f.write(resOutputTrain)

with open("./datasets/500K_20w_s/en-es/dev.en", "w") as f:
    f.write(resInputDev)

with open("./datasets/500K_20w_s/en-es/dev.es", "w") as f:
    f.write(resOutputDev)

with open("./datasets/500K_20w_s/en-es/test.en", "w") as f:
    f.write(resInputTest)

with open("./datasets/500K_20w_s/en-es/test.es", "w") as f:
    f.write(resOutputTest)